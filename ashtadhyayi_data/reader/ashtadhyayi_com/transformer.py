import codecs
import json
import logging
import os
import shutil

import regex

from doc_curation.md.file import MdFile

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
  md_file = MdFile(file_path=outpath, frontmatter_type=MdFile.YAML)
  md_file.dump_to_file(metadata=metadata, md=content, dry_run=dry_run)


def dump_commentary_data(commentary_file_path, suutra_data_path, output_path, dry_run):
  with codecs.open(commentary_file_path) as commentary_file, codecs.open(suutra_data_path) as suutra_data_file:
    if not dry_run:
      shutil.rmtree(output_path, ignore_errors=True)
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


def dump_suutra_basics(indir, outdir, dry_run):
  suutra_data_path = os.path.join(indir, "data.txt")
  logging.info("Transforming sUtra-basics")
  with codecs.open(suutra_data_path) as suutra_data_file:
    suutra_data = json.load(suutra_data_file)["data"]
    for key in ["pc", "ad", "an", "ss"]:
      output_path = os.path.join(outdir, "sUtra-basics", key)
      if not dry_run:
        shutil.rmtree(output_path, ignore_errors=True)
      for suutra in suutra_data:
        dump_suutra_commentary(suutra=suutra, comment=suutra[key], output_path=output_path, dry_run=dry_run)


def separate_commentaries(indir, outdir, dry_run, commentaries_in=None):
  # vartika and data.txt need special treatment - so they're not included below.
  commentaries = ["balamanorama", "bhashya", "kashika", "kaumudi", "laghukaumudi", "nyaas", "padamanjari", "sutrartha", "sutrartha_english", "tattvabodhini"]
  if commentaries_in is not None:
    commentaries = [x for x in commentaries if x in commentaries_in]
  logging.info("Processing commentaries: " + str(commentaries))
  suutra_data_path = os.path.join(indir, "data.txt")
  for commentary in commentaries:
    logging.info("Transforming commentary: %s", commentary)
    commentary_file = os.path.join(indir, "%s.txt" % commentary)
    output_path = os.path.join(outdir, commentary)
    dump_commentary_data(commentary_file_path=commentary_file, suutra_data_path=suutra_data_path, output_path=output_path, dry_run=dry_run)

  if commentaries_in is None or "data" in commentaries_in:
    dump_suutra_basics(indir=indir, outdir=outdir, dry_run=dry_run)


def transform(indir, outdir, dry_run):
  modified_files_json = os.path.join(outdir, "change_details/files_modified.json")
  commentaries = None
  if os.path.exists(modified_files_json):
    with codecs.open(modified_files_json) as f:
      commentaries = [os.path.basename(f).replace(".txt", "") for f in json.load(f) if f.startswith("sutraani")]
      if len(commentaries) == 0:
        logging.info("Must be a dummy commit to trigger regeneration of all commentaries.")
        commentaries = None
      else:
        logging.info("Commentaries to regenerate:" + str(commentaries))
  separate_commentaries(indir=os.path.join(indir, "sutraani"), outdir=os.path.join(outdir, "sUtra-commentaries"), dry_run=dry_run, commentaries_in=commentaries)


# python -c "from ashtadhyayi_data.reader.ashtadhyayi_com import transformer; transformer.separate_commentaries(indir=\"`pwd`/sutraani\", outdir=\"`pwd`/sUtra-commentaries/\", dry_run=True)"
if __name__ == '__main__':
  transform(indir="/home/vvasuki/sanskrit/raw_etexts/vyAkaraNam/aShTAdhyAyI-com-data/", outdir="/home/vvasuki/sanskrit/raw_etexts/vyAkaraNam/aShTAdhyAyI_central-repo/ashtadhyayi_com_transforms", dry_run=True)