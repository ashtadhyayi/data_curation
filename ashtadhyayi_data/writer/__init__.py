import logging
import os

import ashtadhyayi_data
from ashtadhyayi_data.reader.ashtadhyayi_com import api

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s"
)

shared_repo_path = "/home/vvasuki/sanskrit/ashtadhyayi"


def get_output_path(base_dir, vritti_id, sutra_id):
    if vritti_id in ["padachcheda", "full_sutra", "anuvritti", "adhikara", "sumit_garg_english", 'topic']:
        extension = "txt"
    else:
        extension = "md"
    outpath = os.path.join(base_dir, vritti_id, "pada-" + ashtadhyayi_data.get_adhyaya_pada_id(sutra_id), sutra_id + "." + extension)
    return outpath


def dump_tsv_vritti(vritti_id):
    from ashtadhyayi_data.reader import vritti_tsv 
    vritti_tsv.setup_vritti(vritti_id=vritti_id)
    for sutra_id in ashtadhyayi_data.sutra_df.index:
        vritti = vritti_tsv.get_vritti(vritti_id=vritti_id, sutra_id=sutra_id)
        if vritti is not None:
            outpath = get_output_path(base_dir=shared_repo_path, vritti_id=vritti_id, sutra_id=sutra_id)
            os.makedirs(os.path.dirname(outpath),exist_ok=True)
            with open(outpath, 'w', encoding="utf8") as outfile:
                outfile.write(vritti)


if __name__ == '__main__':
    pass
    # dump_tsv_vritti("topic")
    NeeleshSiteExporter.dump_all_from_api("tattvabodhini")
    # delete_empty_vritti_files("padamanjari")