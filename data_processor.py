from marshal import version
import os
import json
from datetime import datetime
from pathlib import Path

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
        version = int(tmp_version)
        return version
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
            version = validate_version(cpe_string, target_vendor, target_product)
            if version is None:
                continue
            key = f"version_{version}"
            value = cve.get("published")
            filtered_data = append_data(filtered_data, key, value)
    return filtered_data


def save_json_data(data, file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
    except FileNotFoundError:
        print(f"File not found: {file_path}")

def load_json_data(file_path):
    data = None
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        data = None
    return data

def append_data(dict,key,value):
    if key in dict:
        dict[key].append(value)
    else:
        dict[key] = [value]
    return dict

def main():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    base_dir = os.path.join(current_dir, "filtered_data")
    source_folder = os.path.join(base_dir, "filtered_cves")

    for path in Path(source_folder).glob("*.json"):
        original_data = load_json_data(path)
        cves = original_data
        filtered_cves = list(filter(lambda x: filter_cve(x, "fedoraproject", "fedora"),cves))
        filtered_data = filter_date_and_versions(filtered_cves, "fedoraproject", "fedora")
        total_filtered_cves += len(filtered_cves)
        print(f"CVEs: {len(filtered_cves)}")
        print(f"current total filtered CVEs: {total_filtered_cves}")

        filtered_json_file_path = os.path.join(base_dir, "filtered_details", "filtered_data.json")
        filtered_json_data = {}
        for key in filtered_data.keys():
            for value in filtered_data[key]:
                filtered_json_data = append_data(filtered_json_data, key, value)
        # save_json_data(filtered_json_data, filtered_json_file_path)

if __name__=="__main__":
    main()