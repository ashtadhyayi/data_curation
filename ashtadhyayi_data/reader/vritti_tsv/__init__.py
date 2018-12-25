import csv
import math
import os
import sys
import pandas
import logging


for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s"
)

vritti_df_map = {}

def setup_vritti(vritti_id):
    vritti_tsv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", vritti_id + ".tsv")
    vritti_df = pandas.read_csv(vritti_tsv_path, sep="\t", keep_default_na=False)
    vritti_df = vritti_df.set_index("index")
    vritti_df_map[vritti_id] = vritti_df
    # exit()


def get_vritti(vritti_id, sutra_id):
    vritti = vritti_df_map[vritti_id].loc[sutra_id, "vritti"]
    return vritti


if __name__ == '__main__':
    setup_vritti("topic")
    get_vritti(sutra_id="1.4.2", vritti_id="topic")