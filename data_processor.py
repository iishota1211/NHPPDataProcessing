from marshal import version
import os
import json
from datetime import datetime

current_dir = os.path.dirname(os.path.realpath(__file__))
base_dir = os.path.join(current_dir, "filtered_data")

cve_source_folder = os.path.join(base_dir, "filtered_cves")
cve_source_file_name = "filtered_nvdcve-2.0-2026.json"
cve_source_dir = os.path.join(cve_source_folder, cve_source_file_name)

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
        print("Invalid string: cannot convert to integer")
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
            version = validate_version(cpe_string, target_vendor, target_product)
            target_vendor, target_product = extract_vendor_product(cpe_string)
            if target_vendor != target_vendor or target_product != target_product:
                continue
            if version is None:
                continue
            key = f"version_{version}"
            value = cve.get("published")
            filtered_data = append_data(filtered_data, key, value)
    return filtered_data


def save_json_data(data, file_dir_name, file_name):
    target_dir = os.path.join(base_dir, file_dir_name)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    file_path = os.path.join(target_dir, file_name)
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
    except FileNotFoundError:
        print(f"File not found: {file_path}")

def load_json_data(file_dir_name, file_name):
    data = None
    file_path = os.path.join(base_dir, file_dir_name, file_name)
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
    data = load_json_data("filtered_cves", "filtered_nvdcve-2.0-2002.json")
    filtered_json_data = load_json_data("filtered_details", "filtered_data.json")
    cves = data
    # print(f"json details: {json.dumps(data, indent=4)}")
    filtered_cves = list(filter(lambda x: filter_cve(x, "fedoraproject", "fedora"),cves))
    filtered_data = filter_date_and_versions(filtered_cves, "fedoraproject", "fedora")
    print(f"Filtered CVEs: {len(filtered_cves)}")
    print(f"Filtered Data: {len(filtered_data)}")

    print(f"Filtered Data: {json.dumps(filtered_data, indent=4)}")
    for key in filtered_data.keys():
        for value in filtered_data[key]:
            print(f"{key}: {value}")
            print(f"type of value: {type(value)}")
    # save_json_data(filtered_json_data, "filtered_details", "filtered_data.json")
    print(f"Filtered json Data: {json.dumps(filtered_json_data, indent=4)}")


if __name__=="__main__":
    main()