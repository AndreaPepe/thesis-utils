import hashlib
import os
import time
import datetime
import vt

API_KEY = "KEY HERE!"

last_call = datetime.datetime.now()


def upload_to_vt(apikey, file_path, skip_check=True):
    with vt.Client(apikey) as client:
        with open(file_path, "rb") as f:
            content = f.read()
            file_hash = hashlib.sha256(content).hexdigest()

        if not skip_check:
            try:
                res = client.get_object(f"/files/{file_hash}")
                print(f"{file_path}: {res.last_analysis_stats}")
            except vt.error.APIError:
                print(f"Never scanned before, uploading {file_path}  to VT...")
                skip_check = True

        if skip_check:
            global last_call
            elapsed = (datetime.datetime.now() - last_call).total_seconds()
            if elapsed < 15:
                time.sleep(15 - elapsed)
            last_call = datetime.datetime.now()

            with open(file_path, "rb") as f:
                analysis = client.scan_file(file=f, wait_for_completion=False)
                print(analysis)


def get_apks_sorted(dir_name):
    list_of_files = [os.path.join(dir_name, x) for x in os.listdir(dir_name) if "stego" not in x]
    list_of_files = filter(lambda x: os.path.isfile(x) and x.endswith(".apk"), list_of_files)
    list_of_files = sorted(list_of_files)
    return list_of_files


def upload_apks_to_vt(dir_name, exclude_until=None):
    apks = get_apks_sorted(dir_name)
    if exclude_until:
        j = -1
        for i, a in enumerate(apks):
            if os.path.abspath(exclude_until) == os.path.abspath(a):
                j = i
        if j == -1:
            print("We didn't find the exclude_until file")
        else:
            apks = apks[j:]

    for f in apks:
        print(f"Processing {f}")
        upload_to_vt(API_KEY, f)


upload_apks_to_vt("/home/pellegrini/Scaricati/ZIPPONE2_LA_VENDETTA/", None)
