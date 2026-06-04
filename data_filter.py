import zipfile
from pathlib import Path
import os 
import json
from utility import *

current_dir = os.path.dirname(os.path.realpath(__file__))

source_folder_name = "json"
source_folder = os.path.join(current_dir, source_folder_name)
source_file_name = "nvdcve-2.0-2026.json"
source_dir = os.path.join(current_dir, source_folder_name, source_file_name)

filtered_data_folder = os.path.join(current_dir, "filtered_data")

total_filtered_cves = 0
for path in Path(source_folder).glob("*.json"):
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        vulnerabilities = data.get("vulnerabilities", [])
        cves = [vulnerability.get("cve") for vulnerability in vulnerabilities]
        print(f"file name: {path.stem}, number of CVEs: {len(cves)}")

        filtered = list(filter(lambda x: filter_cve(x, "fedoraproject", "fedora"),cves))
        print(f"Filtered CVEs: {len(filtered)}")
        total_filtered_cves += len(filtered)
        print(f"current total filtered CVEs: {total_filtered_cves}")
        filename = f"filtered_{path.stem}.json"
        #if len(filtered) > 0:
            #save_json_data(filtered, filename)

print(f"Total filtered CVEs: {total_filtered_cves}")