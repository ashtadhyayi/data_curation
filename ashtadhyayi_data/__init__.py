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
# logging.debug(sutra_df)
