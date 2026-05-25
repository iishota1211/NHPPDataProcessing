from marshal import version
import os
import json
from datetime import datetime

current_dir = os.path.dirname(os.path.realpath(__file__))

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

def find_unique_versions(cves,target_vendor, target_product):
    versions = []
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
            if version is not None and version not in versions:
                versions.append(version)
    return versions

filtered_data_folder = os.path.join(current_dir, "filtered_data")

def save_extracted_data(data, filename):
    if not os.path.exists(filtered_data_folder):
        os.makedirs(filtered_data_folder)
    file_path = os.path.join(filtered_data_folder, filename)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

current_dir = os.path.dirname(os.path.realpath(__file__))

source_folder_name = os.path.join("filtered_data","fedora")
source_folder = os.path.join(current_dir, source_folder_name)
source_file_name = "filtered_nvdcve-2.0-2026.json"
source_dir = os.path.join(current_dir, source_folder_name, source_file_name)



with open(source_dir, 'r', encoding='utf-8') as f:
    data = json.load(f)
    cves = data
    print(f"cve length : {len(data)}")
    filtered_cves = list(filter(lambda x: filter_cve(x, "fedoraproject", "fedora"),cves))
    versions = find_unique_versions(filtered_cves, "fedoraproject", "fedora")
    print(f"Filtered CVEs: {len(filtered_cves)}")
    print(f"Unique Versions: {len(versions)}")
    print(f"Versions: {versions}")

test_data = {}
for i in range(1,10):
    version_key = f"version_{i}"
    test_data[version_key] = []
if test_data.get("version_20") is not None:
    test_data["version_20"].append("CVE-2026-0002")
else:
    test_data["version_20"] = ["CVE-2026-0002"]

save_extracted_data(test_data, "test.json")