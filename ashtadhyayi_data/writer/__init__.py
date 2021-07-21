import logging
import os

import ashtadhyayi_data
from doc_curation.md import library
from doc_curation.md.file import MdFile

for handler in logging.root.handlers[:]:
  logging.root.removeHandler(handler)
logging.basicConfig(
  level=logging.DEBUG,
  format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s"
)

shared_repo_path = "/home/vvasuki/sanskrit/ashtadhyayi"


def get_output_path(base_dir, vritti_id, suutra_id):
  if vritti_id in ["padachcheda", "full_sutra", "anuvritti", "adhikara", "sumit_garg_english", 'topic']:
    extension = "txt"
  else:
    extension = "md"
  outpath = os.path.join(base_dir, vritti_id, "pada-" + ashtadhyayi_data.get_adhyaya_pada_id(suutra_id),
                         suutra_id + "." + extension)
  return outpath


def dump_tsv_vritti(vritti_id):
  from ashtadhyayi_data.reader import vritti_tsv
  vritti_tsv.setup_vritti(vritti_id=vritti_id)
  for suutra_id in ashtadhyayi_data.suutra_df.index:
    vritti = vritti_tsv.get_vritti(vritti_id=vritti_id, suutra_id=suutra_id)
    if vritti is not None:
      outpath = get_output_path(base_dir=shared_repo_path, vritti_id=vritti_id, suutra_id=suutra_id)
      os.makedirs(os.path.dirname(outpath), exist_ok=True)
      with open(outpath, 'w', encoding="utf8") as outfile:
        outfile.write(vritti)


def dump_per_suutra_mds(outpath, dry_run=False):
  md_file = MdFile(file_path="/home/vvasuki/ashtadhyayi/ashtadhyayi.github.io/content/sutra-details.md")
  (_, template_content) = md_file.read_md_file()
  suutra_df = ashtadhyayi_data.get_suutra_df()
  for suutra_id in suutra_df.index:
    dest_path = os.path.join(outpath, ashtadhyayi_data.get_adhyaya_pada_id(suutra_id), "%s.md" % suutra_id)
    md_file = MdFile(file_path=dest_path)
    title = suutra_df.loc[suutra_id, "sutra"]
    title = "%s %s" % (suutra_id, title)
    [adhyaaya, paada, suutra] = suutra_id.split(".")
    content = template_content.replace("ADHYAAYA", adhyaaya).replace("PAADA", paada).replace("SUUTRA", suutra)
    md_file.dump_to_file(metadata={"title": title}, content=content, dry_run=dry_run)
  library.fix_index_files(dir_path=outpath)

if __name__ == '__main__':
  pass
  dump_per_suutra_mds(outpath="/home/vvasuki/ashtadhyayi/ashtadhyayi.github.io/content/suutra/")
  # dump_tsv_vritti("topic")
  # delete_empty_vritti_files("padamanjari")
