"""
it uses above structures to generate babylon files of given vritti
object. ``create_babylon`` function takes optional custom functions, to
customize head_words, content, directives for our requirement. if
custome functions not provided, it uses default functions in same
module.

following is example code.

.. code:: python

   from ashtadhyayi_repo_parser.structures import Vritti, Adhyaaya, Paada, Sutra
   from ashtadhyayi_repo_parser.helpers.babylon_helper import create_babylon

   kashika = Vritti('kashika', root_dir_path='/home/user/path/to/ashtadhyayi/kashika/')

   create_babylon(kashika, babylon_file_path='/home/path/to/kashika.babylon')  # it will save babylon file at babylon_file_path

   # we can provide optional arguments to cutomize output.

"""
from collections import OrderedDict

from mistune import Markdown
from indic_transliteration.sanscript import transliterate, DEVANAGARI, ITRANS

from ashtadhyayi_data.structures import *


def default_babylon_directives_generator(vritti):
    babylon_directives = OrderedDict([
        ("stripmethod", "keep"),
        ("sametypesequence", "h"),
        ("bookname", (vritti.metadata or {}).get('name', None) or vritti.name)
    ])
    return babylon_directives


def default_headwords_generator(sutra):
    try:
        json_doc = sutra.json()
    except Exception as e:
        print('error in reading {}'. format(sutra.index), str(e))
        return None
    index = json_doc.get('index', '')
    index_de = transliterate(index, ITRANS, DEVANAGARI)
    sutra = json_doc.get('sutra', '')
    sutra_itrans = transliterate(sutra, DEVANAGARI, ITRANS).replace('|', '।')
    head_words = [
        index,
        index_de,
        sutra,
        sutra_itrans,
        index + ' ' + sutra_itrans,
        sutra_itrans + ' ' + index,
        index_de + ' ' + sutra,
        sutra + ' ' + index_de
    ]
    head_words = [hw for hw in head_words if hw != '']
    return head_words


def default_content_generator(sutra, markdown_parser=None):
    json_doc = sutra.json()
    markdown_parser = markdown_parser or Markdown()
    content = json_doc['content']
    content_parsed = markdown_parser(content).strip()
    content_parsed = content_parsed.replace('\n', '<BR>').replace('<code>', '<strong>').replace('</code>', '</strong>')
    if content_parsed == '':
        print('sutra {} has no content'.format(sutra.index))
    return content_parsed


def create_babylon(
        vritti, babylon_file_path,
        babylon_directives_generator=default_babylon_directives_generator,
        headwords_generator=default_headwords_generator,
        content_generator=default_content_generator):

    try:
        os.remove(babylon_file_path)
    except FileNotFoundError:
        pass

    babylon_file = open(babylon_file_path, 'ab')
    babylon_file.write('\n'.encode('utf-8'))

    directives = babylon_directives_generator(vritti)
    for key, val in directives.items():
        directive_line = "#{key}={val}\n".format(key=key, val=val)
        babylon_file.write(directive_line.encode('utf-8'))

    babylon_file.write('\n'.encode('utf-8'))

    markdown_parser = Markdown()

    for adhyaaya in vritti:
        for paada in adhyaaya:
            for sutra in paada:
                head_words = headwords_generator(sutra)
                if not head_words:
                    continue
                content = content_generator(sutra, markdown_parser=markdown_parser)
                if not content:
                    continue
                headwords_line = '|'.join(head_words) + '\n'
                content_line = content.strip('\n') + '\n'

                babylon_file.write(headwords_line.encode('utf-8'))
                babylon_file.write(content_line.encode('utf-8'))
                babylon_file.write('\n'.encode('utf-8'))

    babylon_file.close()
