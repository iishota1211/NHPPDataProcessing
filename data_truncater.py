import json
from utility import *
import os
from pathlib import Path
from datetime import datetime

def truncate_by_date_range(data, start_date, end_date):
    truncated_data = []
    for data_point in data:
        timed_data_point = datetime.fromisoformat(data_point)
        if timed_data_point >= start_date and timed_data_point <= end_date:
            truncated_data.append(data_point)
    return truncated_data

def generate_type1_range(file_name, version_detail):
    key = file_name
    next_key = "version_" + str(int(file_name.split("_")[1]) + 1)
    start_date = datetime.fromisoformat(version_detail[key][0])
    if not next_key in version_detail.keys():
        end_date = datetime.fromisoformat(version_detail[key][1])
    else:
        end_date = datetime.fromisoformat(version_detail[next_key][0])
    return start_date, end_date

def generate_type2_range(file_name, version_detail):
    key = file_name
    start_date = datetime.fromisoformat(version_detail[key][0])
    end_date = datetime.fromisoformat(version_detail[key][1])
    return start_date, end_date

def generate_range(dataType, file_name, version_detail):
    if dataType == "Type1":
        return generate_type1_range(file_name, version_detail)
    elif dataType == "Type2":
        return generate_type2_range(file_name, version_detail)
    else:
        raise ValueError(f"Unsupported data type: {dataType}")

def main():
    dataType = "Type2"
    current_dir = os.path.dirname(os.path.realpath(__file__))
    source_folder = os.path.join(current_dir, "filtered_data", "filtered_details", "Type2")
    save_folder_path = os.path.join(current_dir, "filtered_data", "truncated_data", dataType)
    version_detail_path = os.path.join(current_dir, "filtered_data", "version_detail.json")
    version_detail = load_json_data(version_detail_path)

    for path in Path(source_folder).glob("*.json"):
        data = load_json_data(path)
        file_name = path.stem
        if not file_name in version_detail.keys():
            continue

        start_date, end_date = generate_range(dataType, file_name, version_detail)
        truncated_data = truncate_by_date_range(data, start_date, end_date)
        save_json_data(truncated_data, os.path.join(save_folder_path, f"{file_name}.json"))
        for data_point in truncated_data:
            print(f"Data point {data_point} in file {file_name} is within the range ({start_date} - {end_date})")

if __name__=="__main__":
    main()