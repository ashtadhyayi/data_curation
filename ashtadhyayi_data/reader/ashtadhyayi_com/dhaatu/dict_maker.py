import codecs
import json
import logging
import os

import regex
import tqdm

from ashtadhyayi_data.reader.ashtadhyayi_com import dhaatu
from ashtadhyayi_data.reader.ashtadhyayi_com.dhaatu import DHAATU_FILES_DIR, dhaatu_dict


def dump_base_dict(output_path):
  dict_name = "ashtadhyayi_com_dhaatu"
  logging.info("Dumping %s\n", dict_name)
  output_dict_path = os.path.join(output_path, dict_name, "%s.babylon" % dict_name)
  os.makedirs(name=os.path.dirname(output_dict_path), exist_ok=True)
  progress_bar = tqdm.tqdm(total=len(dhaatu.dhaatu_dict), desc="dhAtus", position=0)
  log = tqdm.tqdm(total=0, position=3, bar_format='{desc}')
  with codecs.open(output_dict_path, "w") as dict_file:
    for dhaatu_id, dhaatu_details in dhaatu.dhaatu_dict.items():
      if dhaatu_details["aupadeshik"] == "-":
        headwords = [dhaatu_details["dhatu"]]
      else:
        headwords = [dhaatu_details["dhatu"], dhaatu_details["aupadeshik"]]
      headwords = list( dict.fromkeys(headwords) )
      dict_file.write("%s\n" % "|".join(headwords))
      upasargas = ["%s - %s" % (u["name"], u["artha_hindi"]) for u in dhaatu_details["upasargas"]]
      upasarga_str = possible_list_to_str(upasargas)
      notes_str = possible_list_to_str(dhaatu_details["notes"])
      entry = "%s %s %s<br>%s<br>%s<br>%s<br>%s" % (
        dhaatu_details["dhatu"], dhaatu_details["aupadeshik"], 
        dhaatu_details["artha"].replace("<", "{").replace(">", "}"), 
        dhaatu_details.get("artha_english", "").replace("<", "{").replace(">", "}"), 
        dhaatu_details.get("artha_hindi", "").replace("<", "{").replace(">", "}"),
        notes_str,
        upasarga_str)
      dict_file.write("%s\n\n" % entry)
      # log.set_description_str(dhaatu_id)
    progress_bar.update(1)

def fix_markings(in_str):
  return in_str.replace("<", "{").replace(">", "}")

def possible_list_to_str(value):
  if isinstance(value, list):
    out_str = "<br>".join([fix_markings(item) for item in value])
  else:
    out_str = fix_markings(value)
  return out_str


def dump_forms_dict(type, output_path):
  dict_name = "ashtadhyayi_com_%s" % type
  logging.info("Dumping %s\n", dict_name)
  output_dict_path = os.path.join(output_path, dict_name, "%s.babylon" % dict_name)
  os.makedirs(name=os.path.dirname(output_dict_path), exist_ok=True)
  with codecs.open(os.path.join(DHAATU_FILES_DIR, "dhatuforms_%s.txt" % type), "r") as forms_file:
    forms_dict = json.load(forms_file)
    with codecs.open(output_dict_path, "w") as dict_file:
      progress_bar = tqdm.tqdm(total=len(forms_dict), desc="dhAtus", position=0)
      log = tqdm.tqdm(total=0, position=3, bar_format='{desc}')
      for dhaatu_id, details in forms_dict.items():
        for lakaara, value_str in details.items():
          if value_str.strip() == "":
            continue
          value_str = value_str.replace("​", "")
          forms = regex.split('[;,]', value_str)
          dhaatu_details = dhaatu_dict[dhaatu_id]
          headwords = [dhaatu_details["dhatu"], dhaatu_details["aupadeshik"]]
          headwords.extend(forms)
          headwords = list( dict.fromkeys(headwords) )
          dict_file.write("%s\n" % ("|".join(headwords)))
          forms_table = regex.sub("(.+);(.+);(.+);(.+);(.+);(.+);(.+);(.+);(.+)", r"\1<br>\2<br>\3<br>---<br>\4<br>\5<br>\6<br>---<br>\7<br>\8<br>\9", value_str.replace(",", " / "))
          entry = "%s %s %s %s<br><br>%s" % (dhaatu_details["dhatu"], dhaatu_details["aupadeshik"], dhaatu_details["artha"], dhaatu.get_sanskrit_lakaara(lakaara_code=lakaara), forms_table)
          dict_file.write("%s\n\n" % entry)
          # log.set_description_str(dhaatu_id)
        progress_bar.update(1)


def dump_all_forms(output_path):
  dump_base_dict(output_path=output_path)
  dump_forms_dict(type="nich", output_path=output_path)
  dump_forms_dict(type="san", output_path=output_path)
  dump_forms_dict(type="yang", output_path=output_path)
  dump_forms_dict(type="yangluk", output_path=output_path)


if __name__ == '__main__':
  dump_all_forms(output_path="/home/vvasuki/indic-dict/stardict-sanskrit-vyAkaraNa/")
