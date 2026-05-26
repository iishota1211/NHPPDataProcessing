from marshal import version
import os
import json
from datetime import datetime
from pathlib import Path

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

def main():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    base_dir = os.path.join(current_dir, "filtered_data")
    source_folder = os.path.join(base_dir, "filtered_details")
    source_file_path = os.path.join(source_folder, "filtered_data.json")

    json_data = load_json_data(source_file_path)
    for key in json_data.keys():
        print(f"{key}")

    asc = {k: v for k, v in sorted(json_data.items(), key=lambda item: int(item[0].split("_")[1]))}
    for key in asc.keys():
        tmp_data = sorted(asc[key])
        asc[key] = tmp_data
    save_json_data(asc, os.path.join(source_folder, "filtered_data_sorted.json"))

    print("After sorting:")
    test_key = "version_17"
    for value in asc[test_key]:
        print(f"{test_key} : {value}")

    save_folder_path = os.path.join(base_dir, "filtered_details","Type2")
    for key in asc.keys():
        file_path = os.path.join(save_folder_path, f"{key}.json")
        save_json_data(asc[key], file_path)

if __name__=="__main__":
    main()