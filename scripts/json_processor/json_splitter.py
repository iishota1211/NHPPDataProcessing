from marshal import version
import os
import json
from datetime import datetime
from pathlib import Path
from utility import *

def main():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    base_dir = os.path.join(current_dir, "filtered_data")
    source_folder = os.path.join(base_dir, "filtered_details")
    source_file_path = os.path.join(source_folder, "filtered_data_sorted.json")

    json_data = load_json_data(source_file_path)
    for key in json_data.keys():
        print(f"{key}")

    asc = {k: v for k, v in sorted(json_data.items(), key=lambda item: int(item[0].split("_")[1]))}
    for key in asc.keys():
        tmp_data = sorted(asc[key])
        asc[key] = tmp_data
    #save_json_data(asc, os.path.join(source_folder, "filtered_data_sorted.json"))

    save_folder_path = os.path.join(base_dir, "filtered_details","Type2")
    for key in asc.keys():
        file_path = os.path.join(save_folder_path, f"{key}.json")
        #save_json_data(asc[key], file_path)

    first_value = datetime.fromisoformat(asc['version_7'][0])
    last_value = datetime.fromisoformat(asc['version_7'][-1])

    diff = last_value - first_value
    print(f"First value: {first_value}")
    print(f"Last value: {last_value}")  
    print(f"Difference in days: {diff}")

if __name__=="__main__":
    main()