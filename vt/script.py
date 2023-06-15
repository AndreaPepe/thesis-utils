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
    def __init__(self, csv_name:str) -> None:
        self.csv_name = csv_name
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
            f.write("name,harmless,malicious,suspicious,timeout,type-unsupported,undetected\n")
            for file_name, res in self.results.items():
                # write files' results
                f.write(f"{file_name},{res['harmless']},{res['malicious']},{res['suspicious']},{res['timeout']},{res['type-unsupported']},{res['undetected']}\n")
    


'''
    This function checks if the analysis is completed and if so, it adds the result to the report
    and removes the analysis from the pending_analysis dictionary.
    It returns True if the analysis is completed, False otherwise.
'''
def get_analysis_result(apikey:str, report: ClassificationReport, file_name:str, id:str):
    with vt.Client(apikey, 1) as client:
        res = client.get_object(f"/analyses/{id}")
        if(res.status == "completed"):
            report.add_result(file_name, res.stats)
            report.remove_analysis(file_name)
            return True
        else:
            return False

'''
    This function uploads a file to VirusTotal and adds the analysis to the report
    If the file was never scanned before, it adds the analysis ID to the pending_analysis dictionary.
'''
def upload_to_vt(apikey, report, file_path):
    file_name = os.path.basename(file_path)
    with vt.Client(apikey, 1) as client:
        with open(file_path, "rb") as f:
            # compute the sha256 hash of the file
            content = f.read()
            file_hash = hashlib.sha256(content).hexdigest()

        try:
            # get last analysis, if any
            res = client.get_object(f"/files/{file_hash}")
            report.add_result(file_name, res.last_analysis_stats)
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
    report = ClassificationReport("report.csv")
    # get all files in the malwares directory
    dir_name = "./expanded_malwares/"
    list_of_files = [os.path.join(dir_name, x) for x in os.listdir(dir_name)]
    list_of_files = filter(lambda x: os.path.isfile(x) and x.endswith(".elf"), list_of_files)
    
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
    #main()
    single_file_report()