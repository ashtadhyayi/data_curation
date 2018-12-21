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

sutra_tsv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sutrANi.tsv")
sutra_df = pandas.read_csv(sutra_tsv_path, sep="\t")
sutra_df = sutra_df.set_index("id")
# logging.debug(sutra_df.index)
# exit()

def get_adhyaya_pada_id(sutra_id):
    return ".".join(sutra_id.split(".")[0:2])

if __name__ == '__main__':
    logging.debug(get_adhyaya_pada_id("1.1.1"))