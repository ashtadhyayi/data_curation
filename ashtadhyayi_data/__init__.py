import csv
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

def get_suutra_df():
    suutra_tsv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/sutrANi.tsv")
    suutra_df = pandas.read_csv(suutra_tsv_path, sep="\t")
    suutra_df = suutra_df.set_index("id")
    return suutra_df
    # logging.debug(suutra_df.index)
    # exit()


def get_adhyaya_pada_id(suutra_id):
    return ".".join(suutra_id.split(".")[0:2])


if __name__ == '__main__':
    logging.debug(get_adhyaya_pada_id("1.1.1"))