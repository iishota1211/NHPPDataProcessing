import zipfile
from pathlib import Path
import os 
import json

current_dir = os.path.dirname(os.path.realpath(__file__))

source_folder_name = "json"
source_folder = os.path.join(current_dir, source_folder_name)
source_file_name = "nvdcve-2.0-2026.json"
source_dir = os.path.join(current_dir, source_folder_name, source_file_name)

filtered_data_folder = os.path.join(current_dir, "filtered_data")

def save_extracted_data(data, filename):
    if not os.path.exists(filtered_data_folder):
        os.makedirs(filtered_data_folder)
    file_path = os.path.join(filtered_data_folder, filename)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def extract_vendor_product(cpe_string):
    parts = cpe_string.split(":")

    min_parts = 5
    vendor_index = 3
    product_index = 4

    if len(parts) < min_parts:
        return None, None

    vendor = parts[vendor_index]
    product = parts[product_index]

    return vendor, product

def filter_cve(cve,target_vendor, target_product):
    configurations = cve.get("configurations", {})
    nodes = []
    cpeMatches = []
    for config in configurations:
        nodes.extend(config.get("nodes", []))
    for node in nodes:
        cpeMatches.extend(node.get("cpeMatch", []))
    is_match = False
    for cpeMatch in cpeMatches:
        criteria = cpeMatch.get("criteria", "")
        vendor, product = extract_vendor_product(criteria)
        if vendor == target_vendor and product == target_product:
            is_match = True
            break

    return is_match

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
            #save_extracted_data(filtered, filename)

print(f"Total filtered CVEs: {total_filtered_cves}")