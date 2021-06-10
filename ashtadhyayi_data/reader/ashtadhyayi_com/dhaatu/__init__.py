import codecs
import json
import os

DHAATU_FILES_DIR = "/home/vvasuki/sanskrit/raw_etexts/vyAkaraNam/aShTAdhyAyI-com-data/dhatu"


dhaatu_dict = {}


def set_dhaatu_dict():
  with codecs.open(os.path.join(DHAATU_FILES_DIR, "data.txt"), "r") as dhaatu_file:
    dhaatu_list = json.load(dhaatu_file)["data"]
    for dhaatu in dhaatu_list:
      dhaatu_dict[dhaatu["baseindex"]] = dhaatu


def get_sanskrit_lakaara(lakaara_code):
  import regex
  lakaara = regex.sub("^p", "परस्मैपदि-", lakaara_code)
  lakaara = regex.sub("^a", "आत्मनेपदि-", lakaara)
  lakaara = lakaara.replace("la", "ल").replace("li", "लि").replace("lru", "लृ").replace("lu", "लु").replace("le", "ले").replace("lo", "लो").replace("t", "ट्").replace("vidhi", "विधि").replace("ashir", "आशीर्").replace("ng", "ङ्")
  return lakaara


set_dhaatu_dict()

