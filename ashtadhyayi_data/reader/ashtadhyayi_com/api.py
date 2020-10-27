import json
import logging
import os

import requests

import ashtadhyayi_data

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s"
)

ashtadhyayi_data_repo_path = "/home/vvasuki/ashtadhyayi/ashtadhyayi_org_data"

def get_data_from_dump(suutra_id):
    infile_path = os.path.join(ashtadhyayi_data_repo_path, "jsons", suutra_id + ".json")
    with open(infile_path, 'r', encoding="utf8") as infile:
        try:
            suutra_data = json.load(infile)
            return suutra_data
        except:
            logging.warning(infile_path)
            dump_suutra_data_from_api(output_path=os.path.join(ashtadhyayi_data_repo_path, "jsons/"), suutra_id=suutra_id)
            return get_data_from_dump(suutra_id)


def get_data_from_api(suutra_id, as_json=False):
    url = "http://www.ashtadhyayi.com/sutraani/json.php/" + suutra_id.replace(".", "/")
    response = requests.get(url)
    if response.status_code != 200:
        import time
        time.sleep(5)
        response = requests.get(url)
    response_text = response.text
    if as_json:
        response_json = json.loads(response_text, encoding="utf8")
        return response_json
        # logging.debug(response_json)
    else:
        return response_text

def dump_suutra_data_from_api(output_path, suutra_id):
    os.makedirs(output_path, exist_ok=True)
    suutra_json = get_data_from_api(suutra_id)
    with open(os.path.join(output_path, suutra_id + '.json'), 'w', encoding="utf8") as outfile:
        # json.dump(suutra_json, outfile, indent=2)
        outfile.write(suutra_json)
        # exit()


def dump_api_data(output_path):
    for suutra_id in ashtadhyayi_data.suutra_df.index:
        dump_suutra_data_from_api(output_path, suutra_id)


if __name__ == '__main__':
    # logging.debug(get_data_from_dump("1.1.1"))
    # dump_api_data(output_path= os.path.join(ashtadhyayi_data_repo_path, "jsons/"))
    dump_suutra_data_from_api(output_path=os.path.join(ashtadhyayi_data_repo_path, "jsons/"), suutra_id="3.3.160")