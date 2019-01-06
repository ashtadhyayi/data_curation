"""
This module provides structures ``Vritti``, ``Adhyaaya``, ``Paada``, ``Sutra``.
we have to initialize any of them with related params like root_dir_path
of those structures, etc. then onwards, we can get member structures
from that root structure by index, or iterate over them, etc. following
is example code.

.. code:: python

   from ashtadhyayi_repo_parser.structures import Vritti, Adhyaaya, Paada, Sutra

   kashika = Vritti('kashika', root_dir_path='/home/user/path/to/ashtadhyayi/kashika/')  # takes other optional kwargs too, like custom file_names_handler, members_cache, metadata, etc.
   adhyaaya1 = kashika.adhyaaya(1)  # type: Adhyaaya
   paada1_2 = adhyaaya1.paada(2)
   sutra_1_2_10 = paada1_2.sutra(10)

   # or we can chain them
   sutra_2_3_7 = kashika.adhyaaya(2).paada(3).sutra(7)  # type: Sutra

when initialized, they won't load member objects. member objects will be
automatically created lazily, when requested on each level. and sutra
files will not get loaded, till we accessed.

| each above data structures will have attributes, when applicable:
  ``root_dir_path``: path to it's dir. (Vritti, Adhyaaya, Paada only)
  ``file_path``: path to sutra file. (Sutra only)
| ``index``: like 1, 1.1, 1.3.4, etc. (all)
| ``adhyaaya_index``, ``paada_index``, ``sutra_index``: string indices.
  (all, till their level)

| ``Sutra`` object has additional attributes, related to file content.
  they are: ``markdown()``: content of sutra file. lazily loaded. can be
  cached optionally
| ``json()`` : markdown structure will be parsed into json data
  structure. can be cached with optional parameter. this will be much
  useful, when we want to access data.

Mainly, we can iterate over above data structures, as they are many time
iterables. following is example code.

.. code:: python

   from ashtadhyayi_repo_parser.structures import Vritti, Adhyaaya, Paada, Sutra

   kashika = Vritti('kashika', root_dir_path='/home/user/path/to/ashtadhyayi/kashika/')

   for adhyaaya in kashika:
       print(adhyaaya.index, adhyaaya.root_dir_path)
       for paada in adhyaaya:
           print(paada.index, paada.root_dir_path)
           for sutra in paada:
               print(sutra.json(cache=False))    

this allows to handle repo with ease for all purposes.
"""

import os
import re


class FileNamesHandlerInterface(object):

    def adhyaaya_dir_name_components(self, dir_name):
        pass

    def paada_dir_name_components(self, dir_name):
        pass

    def sutra_file_name_components(self, file_name):
        pass

    def adhyaaya_dir_name(self, adhyaaya):
        pass

    def paada_dir_name(self, adhyaaya, paada):
        pass

    def sutra_file_name(self, adhyaaya, paada, sutra):
        pass


class DefaultFileNamesHandler(FileNamesHandlerInterface):

    adhyaaya_dir_name_regex = r'pada-(?P<adhyaaya>[0-9]*)'  # filler, there is no adhyaaya level, in present repo structure
    paada_dir_name_regex = r'pada-(?P<adhyaaya>[0-9]*).(?P<paada>[0-9]*)'
    sutra_file_name_regex = r'(?P<adhyaaya>[0-9]*).(?P<paada>[0-9]*).(?P<sutra>[0-9]*)'

    @staticmethod
    def _matched_groups_dict(regex, string):
        match = re.match(regex, string)
        if not match:
            return {}
        return match.groupdict()

    def adhyaaya_dir_name_components(self, dir_name):
        return self._matched_groups_dict(self.adhyaaya_dir_name_regex, dir_name)

    def paada_dir_name_components(self, dir_name):
        return self._matched_groups_dict(self.paada_dir_name_regex, dir_name)

    def sutra_file_name_components(self, file_name):
        return self._matched_groups_dict(self.sutra_file_name_regex, file_name)

    def adhyaaya_dir_name(self, adhyaaya):
        return ''  # no adhyaaya level

    def paada_dir_name(self, adhyaaya, paada):
        return 'paada-{adhyaaya}.{paada}'.format(adhyaaya=adhyaaya, paada=paada)

    def sutra_file_name(self, adhyaaya, paada, sutra):
        return '{adhyaaya}.{paada}.{sutra}.md'.format(adhyaaya=adhyaaya, paada=paada, sutra=sutra)


class Vritti(object):

    class_label = 'vritti'

    def __init__(self, name, root_dir_path=None, file_names_handler=None, member_objects_cache=True, metadata=None):
        self.name = name
        self.metadata = metadata
        self.member_objects_cache = member_objects_cache

        self.root_dir_path = root_dir_path
        self.file_names_handler = file_names_handler or DefaultFileNamesHandler()

        self.adhyaaya_dir_names_map = None
        self._adhyaayas = None

        if root_dir_path is not None:
            self.load_structure(root_dir_path, file_names_handler=file_names_handler)

    def load_structure(self, root_dir_path, file_names_handler=None):
        self.root_dir_path = root_dir_path
        self.file_names_handler = file_names_handler or DefaultFileNamesHandler()

        self.adhyaaya_dir_names_map = dict()
        self._adhyaayas = dict()

        if not os.path.exists(self.root_dir_path):
            raise FileNotFoundError('{} does not exist'.format(self.root_dir_path))

        all_dir_names = [
            dir_name for dir_name in os.listdir(root_dir_path)
            if os.path.isdir(os.path.join(self.root_dir_path, dir_name))
        ]
        for dn in all_dir_names:
            components = self.file_names_handler.adhyaaya_dir_name_components(dn)
            if 'adhyaaya' not in components:
                continue
            self.adhyaaya_dir_names_map[components['adhyaaya']] = self.file_names_handler.adhyaaya_dir_name(components['adhyaaya'])

    def adhyaaya(self, adhyaaya_index):
        adhyaaya_index = str(adhyaaya_index)
        if self.adhyaaya_dir_names_map is None:
            return None

        if self.member_objects_cache and adhyaaya_index in self._adhyaayas:
            return self._adhyaayas[adhyaaya_index]

        if adhyaaya_index not in self.adhyaaya_dir_names_map:
            return None

        adhyaaya_dir_path = os.path.join(self.root_dir_path, self.adhyaaya_dir_names_map[adhyaaya_index])
        adhyaaya = Adhyaaya(
            adhyaaya_index, root_dir_path=adhyaaya_dir_path,
            file_names_handler=self.file_names_handler,
            member_objects_cache=self.member_objects_cache
        )
        if adhyaaya is None:
            return None

        if self.member_objects_cache:
            self._adhyaayas[adhyaaya_index] = adhyaaya

        return adhyaaya

    def _adhyaaya_generator(self, reverse=False):
        if self.adhyaaya_dir_names_map is None:
            return None

        adhyaaya_indices = sorted(self.adhyaaya_dir_names_map.keys(), key=int, reverse=reverse)
        for index in adhyaaya_indices:
            yield self.adhyaaya(index)

    def __iter__(self):
        return self._adhyaaya_generator()


class Adhyaaya(object):

    def __init__(
            self, adhyaaya_index, root_dir_path=None, file_names_handler=None,
            member_objects_cache=True, metadata=None):
        self.adhyaaya_index = adhyaaya_index
        self.index = '.'.join([adhyaaya_index])

        self.metadata = metadata
        self.member_objects_cache = member_objects_cache

        self.root_dir_path = root_dir_path
        self.file_names_handler = file_names_handler or DefaultFileNamesHandler()

        self.paada_dir_names_map = None
        self._paadas = None

        if root_dir_path is not None:
            self.load_structure(root_dir_path, file_names_handler)

    def load_structure(self, root_dir_path, file_names_handler):
        self.root_dir_path = root_dir_path
        self.file_names_handler = file_names_handler or DefaultFileNamesHandler()

        self.paada_dir_names_map = dict()
        self._paadas = dict()

        all_dir_names = [
            dir_name for dir_name in os.listdir(root_dir_path)
            if os.path.isdir(os.path.join(self.root_dir_path, dir_name))
        ]
        for dn in all_dir_names:
            components = self.file_names_handler.paada_dir_name_components(dn)
            if 'adhyaaya' in components and components['adhyaaya'] != self.adhyaaya_index:
                continue
            if 'paada' not in components:
                continue
            self.paada_dir_names_map[components['paada']] = dn

    def paada(self, paada_index):
        paada_index = str(paada_index)
        if self.paada_dir_names_map is None:
            return None

        if self.member_objects_cache and paada_index in self._paadas:
            return self._paadas[paada_index]

        if paada_index not in self.paada_dir_names_map:
            return None

        paada_dir_path = os.path.join(self.root_dir_path, self.paada_dir_names_map[paada_index])
        paada = Paada(
            self.adhyaaya_index, paada_index,
            root_dir_path=paada_dir_path,
            file_names_handler=self.file_names_handler,
            member_objects_cache=self.member_objects_cache
        )
        if paada is None:
            return None

        if self.member_objects_cache:
            self._paadas[paada_index] = paada

        return paada

    def _paada_generator(self, reverse=False):
        if self.paada_dir_names_map is None:
            return None

        paada_indices = sorted(self.paada_dir_names_map.keys(), key=int, reverse=reverse)
        for index in paada_indices:
            yield self.paada(index)

    def __iter__(self):
        return self._paada_generator()


class Paada(object):

    def __init__(
            self, adhyaaya_index, paada_index,
            root_dir_path=None, file_names_handler=None,
            member_objects_cache=True, metadata=None):

        self.adhyaaya_index = adhyaaya_index
        self.paada_index = paada_index
        self.index = '.'.join([adhyaaya_index, paada_index])

        self.metadata = metadata
        self.member_objects_cache = member_objects_cache

        self.root_dir_path = root_dir_path
        self.file_names_handler = file_names_handler or DefaultFileNamesHandler

        self.sutra_file_names_map = None
        self._sutras = None

        if root_dir_path is not None:
            self.load_structure(root_dir_path, file_names_handler)

    def load_structure(self, root_dir_path, file_names_handler):
        self.root_dir_path = root_dir_path
        self.file_names_handler = file_names_handler or DefaultFileNamesHandler()

        self.sutra_file_names_map = dict()
        self._sutras = dict()

        all_file_names = [
            dir_name for dir_name in os.listdir(root_dir_path)
            if os.path.isfile(os.path.join(self.root_dir_path, dir_name))
        ]
        for fn in all_file_names:
            components = self.file_names_handler.sutra_file_name_components(fn)
            if 'adhyaaya' in components and components['adhyaaya'] != self.adhyaaya_index:
                continue
            if 'paada' in components and components['paada'] != self.paada_index:
                continue
            if 'sutra' not in components:
                continue

            self.sutra_file_names_map[components['sutra']] = fn

    def sutra(self, sutra_index):
        sutra_index = str(sutra_index)
        if self.sutra_file_names_map is None:
            return None

        if self.member_objects_cache and sutra_index in self._sutras:
            return self._sutras[sutra_index]

        if sutra_index not in self.sutra_file_names_map:
            return None

        sutra_file_path = os.path.join(self.root_dir_path, self.sutra_file_names_map[sutra_index])

        sutra = Sutra(
            self.adhyaaya_index, self.paada_index, sutra_index,
            file_path=sutra_file_path,
            file_names_handler=self.file_names_handler,
            member_objects_cache=self.member_objects_cache
        )
        if sutra is None:
            return None

        if self.member_objects_cache:
            self._sutras[sutra_index] = sutra

        return sutra

    def _sutra_generator(self, reverse=False):
        if self.sutra_file_names_map is None:
            return None

        sutra_indices = sorted(self.sutra_file_names_map.keys(), key=int, reverse=reverse)
        for index in sutra_indices:
            yield self.sutra(index)

    def __iter__(self):
        return self._sutra_generator()


class Sutra(object):

    def __init__(
            self, adhyaaya_index, paada_index, sutra_index,
            file_path=None, file_names_handler=None,
            member_objects_cache=True, metadata=None):

        self.adhyaaya_index = adhyaaya_index
        self.paada_index = paada_index
        self.sutra_index = sutra_index
        self.index = '.'.join([adhyaaya_index, paada_index, sutra_index])

        self.metadata = metadata
        self.member_objects_cache = member_objects_cache

        self.file_path = file_path
        self.file_names_handler = file_names_handler

        self._markdown = None
        self._json = None

        if file_path is not None:
            self.load_structure(file_path=file_path, file_names_handler=file_names_handler)

    def markdown(self, cache=False):
        if self.file_path is None:
            return None
        if cache and self._markdown:
            return self._markdown
        try:
            markdown_doc = open(self.file_path, 'rb').read().decode('utf-8')
        except Exception as e:
            print({"file_path": self.file_path})
            raise e

        if cache:
            self._markdown = markdown_doc
        return markdown_doc

    def json(self, cache=False):
        if self.file_path is None:
            return None
        if cache and self._json:
            return self._json
        markdown_doc = self.markdown(cache=cache)
        json_doc = self.md2json(markdown_doc)
        if cache:
            self._json = json_doc
        return json_doc

    @classmethod
    def md2json(cls, md_doc):
        json_doc = {}
        lines = md_doc.split('\n')
        lines_iterator = iter(lines)

        line1 = next(lines_iterator)
        if re.match(r'--- *$', line1):
            for line in lines_iterator:
                line = line.strip()
                if re.match(r'--- *$', line):
                    break
                line_parts = line.split(':', maxsplit=1)
                if len(line_parts) == 2:
                    json_doc[line_parts[0].strip()] = line_parts[1].strip()
            json_doc['content'] = '\n'
        else:
            json_doc['content'] = line1 + '\n'

        json_doc['content'] = (json_doc['content'] + '\n'.join(lines_iterator)).strip()

        return json_doc

    def load_structure(self, file_path, file_names_handler):
        self.file_path = file_path
        self.file_names_handler = file_names_handler or DefaultFileNamesHandler()
