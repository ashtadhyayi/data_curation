import logging
import os

import ashtadhyayi_data
from ashtadhyayi_data.reader import ashtadhyayi_org
from ashtadhyayi_data.reader.ashtadhyayi_org import api

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s"
)

shared_repo_path = "/home/vvasuki/sanskrit/ashtadhyayi"

def get_output_path(vritti_id, sutra_id):
    if vritti_id in ["padachcheda", "full_sutra", "anuvritti", "adhikara"]:
        extension = "txt"
    else:
        extension = "md"
    outpath = os.path.join(shared_repo_path, vritti_id, "pada-" + ashtadhyayi_data.get_adhyaya_pada_id(sutra_id), sutra_id + "." + extension)
    return outpath

def dump_all_from_ashtadhyayi_org_api(vritti_id):
    for sutra_id in ashtadhyayi_data.sutra_df.index:
        sutra_json = api.get_data_from_dump(sutra_id)
        outpath = get_output_path(vritti_id=vritti_id, sutra_id=sutra_id)
        os.makedirs(os.path.dirname(outpath),exist_ok=True)
        vrittiindex = None
        if vritti_id + "_index" in sutra_json:
            vrittiindex = sutra_json[vritti_id + "_index"]
        if sutra_json[vritti_id] == "":
            logging.warning("Skipping " + sutra_id)
        else:
            with open(outpath, 'w', encoding="utf8") as outfile:
                # json.dump(sutra_json, outfile, indent=2)
                if str(outfile).endswith(".md"):
                    outfile.write("---" + "\n")
                    outfile.write("index: " + sutra_id + "\n")
                    outfile.write("sutra: " + ashtadhyayi_data.sutra_df.loc[sutra_id, "sutra"] + "\n")
                    outfile.write("vritti: " + vritti_id + "\n")
                    if vrittiindex is not None:
                        outfile.write("vrittiindex: " + vrittiindex + "\n")
                    outfile.write("---" + "\n" + "\n")
                outfile.write(sutra_json[vritti_id])
                # exit()


def delete_empty_vritti_files(vritti_id):
    for sutra_id in ashtadhyayi_data.sutra_df.index:
        sutra_json = api.get_data_from_dump(sutra_id)
        outpath = get_output_path(vritti_id=vritti_id, sutra_id=sutra_id)
        if sutra_json[vritti_id] == "":
            os.remove(outpath)


if __name__ == '__main__':
    pass
    # dump_all_from_ashtadhyayi_org_api("full_sutra")
    # dump_all_from_ashtadhyayi_org_api("anuvritti")
    # dump_all_from_ashtadhyayi_org_api("adhikara")
    # dump_all_from_ashtadhyayi_org_api("padachcheda")
    # delete_empty_vritti_files("padamanjari")