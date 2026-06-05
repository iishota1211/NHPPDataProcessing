from marshal import version
import os
import json
from datetime import datetime
from pathlib import Path
from utility import *

def validate_version(cpe_string, target_vendor, target_product):
    vendor, product = extract_vendor_product(cpe_string)
    if vendor != target_vendor or product != target_product:
        return None
    
    parts = cpe_string.split(":")
    min_parts = 5
    if len(parts) < min_parts:
        return None
    
    version_index = 5
    tmp_version = parts[version_index]
    try:
        version_number = int(tmp_version)
        return version_number
    except ValueError:
        return None

def filter_date_and_versions(cves,target_vendor, target_product):
    filtered_data = {}
    for cve in cves:
        configurations = cve.get("configurations", {})
        nodes = []
        cpeMatches = []
        for config in configurations:
            nodes.extend(config.get("nodes", []))
        for node in nodes:
            cpeMatches.extend(node.get("cpeMatch", []))
        for cpeMatch in cpeMatches:
            cpe_string = cpeMatch.get("criteria", "")
            vendor, product = extract_vendor_product(cpe_string)
            if vendor != target_vendor or product != target_product:
                continue
            version_number = validate_version(cpe_string, target_vendor, target_product)
            if version_number is None:
                continue
            key = f"version_{version_number}"
            value = cve.get("published")
            filtered_data = append_data(filtered_data, key, value)
    return filtered_data

def main():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    base_dir = os.path.join(current_dir, "filtered_data")
    source_folder = os.path.join(base_dir, "filtered_cves")

    for path in Path(source_folder).glob("*.json"):
        original_data = load_json_data(path)
        cves = original_data
        filtered_cves = list(filter(lambda x: filter_cve(x, "fedoraproject", "fedora"),cves))
        filtered_data = filter_date_and_versions(filtered_cves, "fedoraproject", "fedora")

        filtered_json_file_path = os.path.join(base_dir, "filtered_details", "filtered_data.json")
        filtered_json_data = {}
        for key in filtered_data.keys():
            for value in filtered_data[key]:
                filtered_json_data = append_data(filtered_json_data, key, value)
        # save_json_data(filtered_json_data, filtered_json_file_path)

if __name__=="__main__":
    main()