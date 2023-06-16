import hashlib
import os
import vt
import time
import datetime
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
last_call = datetime.datetime.now()

'''
    This class is used to store the results of the analysis of a set of files
    from VirusTotal and produce a report in CSV file format.
    It has the following fields:
        - csv_name: the name of the csv file where the results will be written
        - results: a dictionary that maps a file name to its results
        - pending_analysis: a dictionary that maps a file name to its analysis id, for those files which were never scanned before on VT
'''
class ClassificationReport:
    def __init__(self, csv_name:str, av_csv:str) -> None:
        self.csv_name = csv_name
        self.av_csv = av_csv
        self.av_results = {}
        self.results = {}
        self.pending_analysis = {}
        

    def add_analysis(self, file_name:str, analysis_id:str):
        self.pending_analysis[file_name] = analysis_id

    def remove_analysis(self, file_name:str):
        del self.pending_analysis[file_name]

    def add_result(self, file_name:str, result):
        self.results[file_name] = result

    def to_csv(self):
        with open(self.csv_name, "w") as f:
            # write the csv header
            f.write("name,harmless,malicious,suspicious,failure,timeout,type-unsupported,undetected,detection rate\n")
            for file_name, attributes in self.results.items():

                try:
                    res = attributes["last_analysis_stats"]
                except KeyError:
                    res = attributes["stats"]

                # write files' results
                # type-unsupported is not taken into account in the detection rate
                sum = res["harmless"] + res["malicious"] + res["suspicious"] + res["failure"] + res["timeout"] + res["undetected"]
                detection_rate = round(((res["malicious"]) / sum), 2) if sum != 0 else 0
                f.write(f"{file_name},{res['harmless']},{res['malicious']},{res['suspicious']},{res['failure']},{res['timeout']},{res['type-unsupported']},{res['undetected']},{detection_rate}\n")
    
                # adjust the anti-virus behaviours
                try:
                    av = attributes["last_analysis_results"]
                except KeyError:
                    av = attributes["results"]

                for av_name, av_res in av.items():
                    if av_name not in self.av_results:
                        self.av_results[av_name] = {"harmless":0, "malicious":0, "suspicious":0, "failure":0, "timeout":0, "type-unsupported":0, "undetected":0}
                    try:
                        self.av_results[av_name][av_res["category"]] += 1
                    except KeyError:
                        self.av_results[av_name]["timeout"] += 1
        
        # compute miss-detection rate of AVs
        for av_name, av_res in self.av_results.items():
            # type-unsupported is not taken into account in the detection rate
            sum = res["harmless"] + res["malicious"] + res["suspicious"] + res["failure"] + res["timeout"] + res["undetected"]
            detection_rate = round(((av_res["malicious"]) / sum), 2) if sum != 0 else 0
            self.av_results[av_name]["detection rate"] = detection_rate

        with open(self.av_csv, "w") as f:
            f.write("name,harmless,malicious,suspicious,failure,timeout,type-unsupported,undetected,detection rate\n")
            for av_name, av_res in self.av_results.items():
                f.write(f"{av_name},{av_res['harmless']},{av_res['malicious']},{av_res['suspicious']},{av_res['failure']},{av_res['timeout']},{av_res['type-unsupported']},{av_res['undetected']},{av_res['detection rate']}\n")


'''
    This function checks if the analysis is completed and if so, it adds the result to the report
    and removes the analysis from the pending_analysis dictionary.
    It returns True if the analysis is completed, False otherwise.
'''
def get_analysis_result(apikey:str, report: ClassificationReport, file_name:str, id:str):
    with vt.Client(apikey, 1) as client:
        res = client.get_json(f"/analyses/{id}")
        if(res['data']['attributes']['status'] == "completed"):
            report.add_result(file_name, res["data"]["attributes"])
            report.remove_analysis(file_name)
            return True
        else:
            return False

'''
    This function uploads a file to VirusTotal and adds the analysis to the report
    If the file was never scanned before, it adds the analysis ID to the pending_analysis dictionary.
'''
def upload_to_vt(apikey:str, report:ClassificationReport, file_path:str):
    file_name = os.path.basename(file_path)
    with vt.Client(apikey, 1) as client:
        with open(file_path, "rb") as f:
            # compute the sha256 hash of the file
            content = f.read()
            file_hash = hashlib.sha256(content).hexdigest()

        try:
            # get last analysis, if any
            res = client.get_json(f"/files/{file_hash}")
            report.add_result(file_name, res["data"]["attributes"])
        except vt.error.APIError:
            print(f"\tNever scanned before, uploading {file_name} to VirusTotal...")
            global last_call
            elapsed = (datetime.datetime.now() - last_call).total_seconds()
            if elapsed < 15:
                time.sleep(15 - elapsed)
            last_call = datetime.datetime.now()

            with open(file_path, "rb") as f:
                analysis = client.scan_file(file=f, wait_for_completion=False)
                print(f"\tPending analysis for {file_name} with id {analysis.id}")
                report.add_analysis(file_name, analysis.id)

def main():
    report = ClassificationReport("report.csv", "av_report.csv")
    # get all files in the malwares directory
    # TODO: configure the directory name
    dir_name = "./malwares_3/"
    list_of_files = [os.path.join(dir_name, x) for x in os.listdir(dir_name)]
    list_of_files = filter(lambda x: os.path.isfile(x), list_of_files)
    #list_of_files = filter(lambda x: not x.startswith('.'), list_of_files)
    list_of_files = sorted(list_of_files)
    # upload files to VirusTotal for scanning
    for f in list_of_files:
        print(f"[+] Processing {f}")
        upload_to_vt(API_KEY, report, f)

    # wait for all pending analysis to complete
    print("\n[+] Waiting for pending analysis...")
    while len(report.pending_analysis) > 0:
        for file_name, analysis_id in list(report.pending_analysis.items()):
            if get_analysis_result(API_KEY, report, file_name, analysis_id):
                print(f"\tAnalysis completed for {file_name}")
        time.sleep(15)

    # write the report to a csv file
    print("[+] Writing csv report...")
    report.to_csv()


def single_file_report():
    file = "../../morphVM/test/expand/test_executable"
    file_name = os.path.basename(file)
    with vt.Client(API_KEY, 1) as client:
        with open(file, "rb") as f:
            # compute the sha256 hash of the file
            content = f.read()
            file_hash = hashlib.sha256(content).hexdigest()

        try:
            # get last analysis, if any
            res = client.get_json(f"/files/{file_hash}")
            print(json.dumps(res, indent=2))
        except vt.error.APIError:
            print(f"\tNever scanned before, uploading {file_name} to VirusTotal...")
            with open(file, "rb") as f:
                analysis = client.scan_file(file=f, wait_for_completion=True)
                print(analysis)
                time.sleep(15)
                res = client.get_json(f"/analyses/{analysis.id}")
                print(json.dumps(res, indent=2))

if __name__=="__main__":
    main()
    #single_file_report()