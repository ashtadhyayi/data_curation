import glob
import os
import pandas

import frontmatter
import logging

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s"
)

ASHTADHYAYI_REPO_ROOT = "/home/vvasuki/sanskrit/ashtadhyayi"

def get_file_paths(vritti_id):
    return sorted(glob.glob(os.path.join(ASHTADHYAYI_REPO_ROOT, vritti_id, "*/*.md")))

def get_vritti_sequence_map(vritti_id):
    vritti_df = pandas.DataFrame(columns= ["index", "sutra", "vritti_index"])
    for file_path in get_file_paths(vritti_id=vritti_id):
        with open(file_path) as f:
            vritti_data = frontmatter.load(f)
            vritti_df.loc[vritti_data["index"]] = [vritti_data["index"], vritti_data["sutra"], None]
            if "vritti_index" in vritti_data:
                vritti_df.loc[vritti_data["index"], "vritti_index"] = vritti_data["vritti_index"]
            # logging.debug(vritti_data)
    vritti_df.set_index("index")
    logging.debug(vritti_df.loc["1.1.1"])


if __name__ == '__main__':
    get_vritti_sequence_map(vritti_id='balamanorama')