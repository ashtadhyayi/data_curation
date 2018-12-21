import json

import requests
import logging
import ashtadhyayi_data
import os
import html
from ratelimit import limits, sleep_and_retry

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s"
)


@sleep_and_retry
@limits(calls=240, period=60)
def get_data(sutra_id, as_json=False):
    url = "http://www.ashtadhyayi.com/sutraani/json.php/" + sutra_id.replace(".", "/")
    response = requests.get(url)
    response_text = response.text
    if as_json:
        response_json = json.loads(response_text, encoding="utf8")
        return response_json
        # logging.debug(response_json)
    else:
        return response_text


def dump_api_data(output_path):
    os.makedirs(output_path, exist_ok=True)
    for sutra_id in ashtadhyayi_data.sutra_df["id"]:
        sutra_json = get_data(sutra_id)
        with open(os.path.join(output_path, sutra_id + '.json'), 'w', encoding="utf8") as outfile:
            # json.dump(sutra_json, outfile, indent=2)
            outfile.write(sutra_json)
            # exit()



if __name__ == '__main__':
    # get_data("1.1.1")
    # logging.debug(ashtadhyayi_data.sutra_ids)
    dump_api_data(output_path="/home/vvasuki/ashtadhyayi/ashtadhyayi_org_data/jsons/")