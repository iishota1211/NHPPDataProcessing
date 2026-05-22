import zipfile
from pathlib import Path
import os 
import json

current_dir = os.path.dirname(os.path.realpath(__file__))
source_folder_name = "json"
source_file_name = "nvdcve-2.0-2026.json"
source_dir = os.path.join(current_dir, source_folder_name, source_file_name)

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

with open(source_dir, 'r', encoding='utf-8') as file:
    data = json.load(file)
    vulnerabilities = data.get("vulnerabilities", [])
    cves = [vulnerability.get("cve") for vulnerability in vulnerabilities]
    cve = cves[0]
    print(f"keys in cve: {cve.keys()}")    

    filtered = list(filter(lambda x: filter_cve(x, "microsoft", "windows"),cves))
    print(f"Filtered CVEs: {len(filtered)}")
        
