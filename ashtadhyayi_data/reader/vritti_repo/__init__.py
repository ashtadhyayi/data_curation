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

pandas.set_option('display.max_columns', 5)
pandas.set_option('display.width', 1000)
ASHTADHYAYI_REPO_ROOT = "/home/vvasuki/sanskrit/ashtadhyayi"

def get_file_paths(vritti_id):
    return sorted(glob.glob(os.path.join(ASHTADHYAYI_REPO_ROOT, vritti_id, "*/*.md")))

def get_vritti_metadata_df(vritti_id):
    vritti_df = pandas.DataFrame(columns= ["index", "sutra", "vritti_index"])
    for file_path in get_file_paths(vritti_id=vritti_id):
        with open(file_path) as f:
            vritti_data = frontmatter.load(f)
            vritti_df.loc[vritti_data["index"]] = [vritti_data["index"], vritti_data["sutra"], None]
            if "vritti_index" in vritti_data:
                vritti_df.loc[vritti_data["index"], "vritti_index"] = vritti_data["vritti_index"]
            # logging.debug(vritti_data)
    vritti_df.set_index("index")
    return vritti_df
    # logging.debug(vritti_df.loc["1.1.1"])

def get_vrittis_with_mismatching_sutra(vritti_id):
    vritti_metadata_df = get_vritti_metadata_df(vritti_id=vritti_id)
    from ashtadhyayi_data import sutra_df
    filtered_df = vritti_metadata_df[vritti_metadata_df["sutra"].replace(to_replace="[ ऽ]", regex=True, value="") != sutra_df.loc[vritti_metadata_df["index"], 'sutra'].replace(to_replace="[ ऽ]", regex=True, value="")]
    logging.debug(filtered_df)
    pass


if __name__ == '__main__':
    get_vrittis_with_mismatching_sutra(vritti_id='balamanorama')