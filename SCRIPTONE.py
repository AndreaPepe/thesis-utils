import hashlib
import json
import os
import datetime
import vt

API_KEY = "KEY HERE!"

last_call = datetime.datetime.now()


def retrieve_from_vt(apikey, file_path):
    with vt.Client(apikey) as client:
        with open(file_path, "rb") as f:
            content = f.read()
            file_hash = hashlib.sha256(content).hexdigest()
        try:
            res = client.get_object(f"/files/{file_hash}")
            return res.last_analysis_stats
        except vt.error.APIError:
            print(f"Never scanned before {file_path}, DA HELL")
            return None


def get_apks_sorted(dir_name):
    list_of_files = [os.path.join(dir_name, x) for x in os.listdir(dir_name) if "stego" not in x]
    list_of_files = filter(lambda x: os.path.isfile(x) and x.endswith(".apk"), list_of_files)
    list_of_files = sorted(list_of_files)
    return list_of_files


def retrieve_folder_from_vt(dir_name):
    apks = get_apks_sorted(dir_name)
    results = []
    for f in apks:
        print(f"Processing {f}")
        r = retrieve_from_vt(API_KEY, f)
        if r is None:
            continue
        _, name = os.path.split(f)
        _, apk_id, malw_id = name[:-4].split("_")
        r["apk_id"] = int(apk_id)
        r["malw_id"] = int(malw_id)
        results.append(r)

    with open("results.json", "w", encoding="utf8") as f:
        json.dump(results, f)


retrieve_folder_from_vt("ZIPPONE2_LA_VENDETTA")
