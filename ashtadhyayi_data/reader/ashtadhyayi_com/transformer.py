import codecs
import json
import logging
import os

import regex
from doc_curation import md_helper

import ashtadhyayi_data
from ashtadhyayi_data import writer

for handler in logging.root.handlers[:]:
  logging.root.removeHandler(handler)
logging.basicConfig(
  level=logging.DEBUG,
  format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s"
)


def markdownify(content):
  content = regex.sub(r"\r?\n", "\n\n", content)
  content = regex.sub("<<", "_", content)
  content = regex.sub(">>", "_", content)
  content = regex.sub("##", "  \n", content)
  content = regex.sub("##", "  \n", content)
  content = regex.sub(r"\$(\d)\$(\d)\$(\d+)", " ($1.$2.$3)", content)
  content = regex.sub(r"\$(\d)(\d)0*(\d+)", " ($1.$2.$3)", content)
  return content


def dump_suutra_commentary(suutra, comment, output_path, dry_run):
  if len(comment) == 0:
    return 
  suutra_index = "%s.%s.%s" % (suutra["a"], suutra["p"], suutra["n"])
  outpath = os.path.join(output_path, "pada-%s.%s/%s.md" % (suutra["a"], suutra["p"], suutra_index))
  metadata = {"index": suutra_index, "sutra": suutra["s"]}
  # logging.debug(metadata)
  # logging.debug(comment)
  content = markdownify(comment)
  md_file = md_helper.MdFile(file_path=outpath, frontmatter_type=md_helper.MdFile.YAML)
  md_file.dump_to_file(metadata=metadata, md=content, dry_run=dry_run)


def dump_commentary_data(commentary_file_path, suutra_data_path, output_path, dry_run):
  with codecs.open(commentary_file_path) as commentary_file, codecs.open(suutra_data_path) as suutra_data_file:
    comments = json.load(commentary_file)
    suutra_data = json.load(suutra_data_file)["data"]
    for suutra in suutra_data:
      comment = comments.get(suutra["i"], None)
      if comment is not None:
        if isinstance(comment, str):
          dump_suutra_commentary(suutra=suutra, comment=comment, output_path=output_path, dry_run=dry_run)
        elif isinstance(comment, dict):
          for key in comment:
            dump_suutra_commentary(suutra=suutra, comment=comment[key], output_path=os.path.join(output_path, key), dry_run=dry_run)


def separate_commentaries(indir, outdir, dry_run):
  commentaries = ["balamanorama", "bhashya", "kashika", "kaumudi", "laghukaumudi", "nyaas", "padamanjari", "sutrartha", "sutrartha_english", "tattvabodhini", "vartika"]
  suutra_data_path = os.path.join(indir, "data.txt")
  for commentary in commentaries:
    commentary_file = os.path.join(indir, "%s.txt" % commentary)
    output_path = os.path.join(outdir, commentary)
    dump_commentary_data(commentary_file_path=commentary_file, suutra_data_path=suutra_data_path, output_path=output_path, dry_run=dry_run)

  with codecs.open(suutra_data_path) as suutra_data_file:
    suutra_data = json.load(suutra_data_file)["data"]
    for key in ["pc", "ad", "an", "ss"]:
      output_path = os.path.join(outdir, "sUtra-basics", key)
      for suutra in suutra_data:
        dump_suutra_commentary(suutra=suutra, comment=suutra[key], output_path=output_path, dry_run=dry_run)


def transform(indir, outdir, dry_run):
  separate_commentaries(indir=os.path.join(indir, "sutraani"), outdir=os.path.join(outdir, "sUtra-commentaries"), dry_run=True)


# python -c "from ashtadhyayi_data.reader.ashtadhyayi_com import transformer; transformer.separate_commentaries(indir=\"`pwd`/sutraani\", outdir=\"`pwd`/sUtra-commentaries/\", dry_run=True)"
if __name__ == '__main__':
  transform(indir="/home/vvasuki/sanskrit/raw_etexts/vyAkaraNam/aShTAdhyAyI-com-data/", outdir="/home/vvasuki/sanskrit/raw_etexts/vyAkaraNam/aShTAdhyAyI_central-repo/ashtadhyayi_com_transforms", dry_run=True)