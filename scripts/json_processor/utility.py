import os
import json
import pandas as pd

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

def append_data(data, key, value):
    if key in data:
        data[key].append(value)
    else:
        data[key] = [value]
    return data

def save_to_excel(data, file_path):
    df = pd.DataFrame(data)
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    
    with pd.ExcelWriter(file_path) as writer:
        df.to_excel(writer, index=False, header=False)

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