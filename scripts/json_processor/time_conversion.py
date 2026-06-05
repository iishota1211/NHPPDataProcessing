import json
from utility import *
import os
from pathlib import Path
from datetime import datetime

def convert_to_timed_data(data,initial_time,time_scale):
    timed_data = []
    for data_point in data:
        timed_data_point = datetime.fromisoformat(data_point)
        if time_scale <= 0:
            raise ValueError(f"Time scale must be positive, but got {time_scale}")
        timed_data.append(int((timed_data_point - initial_time).total_seconds() / time_scale))
    return timed_data

def select_time_scale():
    time_scale_str = input("Please enter the time scale (seconds:1, minutes:2, hours:3, days:4, weeks:5, months:6, years:7): ")

    second = 1
    minute = second * 60
    hour = minute * 60
    day = hour * 24
    week = day * 7
    month = day * 30
    year = day * 365
    time_scale_list = [second, minute, hour, day, week, month, year]
    try:
        time_scale = int(time_scale_str)
        if time_scale <= 0:
            raise ValueError("Time scale must be a positive number.")
        if time_scale > 7:
            raise ValueError("Time scale must be between 1 and 7.")
        return time_scale_list[time_scale - 1]
    except ValueError as e:
        print(f"Invalid input: {e}")
        return select_time_scale()

def select_version_range():
    version_range = input("Please select the version range (e.g., 1-5): ")
    try:
        start_version, end_version = map(int, version_range.split("-"))
        if start_version > end_version:
            raise ValueError("Start version must be less than or equal to end version.")
        return start_version, end_version
    except ValueError as e:
        print(f"Invalid input: {e}")
        return select_version_range()
    
def select_initial_time_from_file(version_detail,dataType):
    version_num = select_version_number_from_user(version_detail)
    file_name = f"version_{version_num}"

    if file_name in version_detail:
        initial_time_str = version_detail[file_name][0]
        try:
            return datetime.fromisoformat(initial_time_str)
        except ValueError as e:
            print(f"Invalid date format for initial time in file {file_name}: {e}")
            raise
    else:
        raise KeyError(f"File name {file_name} not found in version detail.")
    
def select_version_number_from_user(version_detail):
    file_version_num = input("Please enter the file version number for initial time selection: ")
    file_name = f"version_{file_version_num}"
    last_version_num = max([int(key.split("_")[1]) for key in version_detail.keys()])
    if file_name in version_detail:
        return int(file_version_num)
    else:
        print(f"File name {file_name} not found in version detail. Please enter a valid version number (1-{last_version_num}).")
        return select_version_number_from_user(version_detail)

def select_initial_time_from_user():
    initial_time_str = input("Please enter the initial time (in ISO format, e.g., 2023-01-01T00:00:00): ")
    try:
        return datetime.fromisoformat(initial_time_str)
    except ValueError as e:
        print(f"Invalid date format: {e}")
        return select_initial_time_from_user()
    
def select_initial_time(version_detail, dataType):
    choice = input("Choose initial time source (version file:1, user input:2): ").lower()
    if choice == "1":
        return select_initial_time_from_file(version_detail, dataType)
    elif choice == "2":
        return select_initial_time_from_user()
    else:
        print("Invalid choice. Please enter '1' or '2'.")
        return select_initial_time(version_detail, dataType)

def is_in_version_range(file_name, start_version, end_version):
    try:
        version_number = int(file_name.split("_")[1])
        return start_version <= version_number <= end_version
    except (IndexError, ValueError) as e:
        print(f"Invalid file name format: {file_name}. Expected format: 'version_X.json'. Error: {e}")
        return False
    
def ask_save_json_data():
    choice = input("Do you want to save the timed data to JSON files? (yes:1, no:2): ").lower()
    if choice == "1":
        return True
    elif choice == "2":
        return False
    else:
        print("Invalid choice. Please enter '1' or '2'.")
        return ask_save_json_data()
    
def ask_save_excel_data():
    choice = input("Do you want to save the timed data to Excel files? (yes:1, no:2): ").lower()
    if choice == "1":
        return True
    elif choice == "2":
        return False
    else:
        print("Invalid choice. Please enter '1' or '2'.")
        return ask_save_excel_data()
    
def save_json_data_conditionally(data, file_path,is_save):
    if is_save:
        save_json_data(data, file_path)
        print(f"json Timed data saved to {file_path}")


def save_excel_data_conditionally(data, file_path, is_save):
    if is_save:
        save_to_excel(data, file_path)
        print(f"Excel Timed data saved to {file_path}")

def select_data_type():
    choice = input("Please select the data type (Type1:1, Type2:2): ").lower()
    if choice == "1":
        return "Type1"
    elif choice == "2":
        return "Type2"
    else:
        print("Invalid choice. Please enter '1' or '2'.")
        return select_data_type()


def find_time_scale(time_scale):
    second = 1
    minute = second * 60
    hour = minute * 60
    day = hour * 24
    week = day * 7
    month = day * 30
    year = day * 365
    time_scale_dict = {"second": second, "minute": minute, "hour": hour, "day": day, "week": week, "month": month, "year": year}

    if time_scale in time_scale_dict.values():
        for key, value in time_scale_dict.items():
            if value == time_scale:
                return key

def main():
    dataType = select_data_type()
    current_dir = os.path.dirname(os.path.realpath(__file__))
    json_source_folder = os.path.join(current_dir, "filtered_data", "truncated_data", dataType)
    json_save_folder_base_path = os.path.join(current_dir, "filtered_data", "timed_data", dataType)
    version_detail_path = os.path.join(current_dir, "filtered_data", "version_detail.json")
    version_detail = load_json_data(version_detail_path)

    start_version, end_version = select_version_range()
    initial_time = select_initial_time(version_detail, dataType)
    time_scale = select_time_scale()
    is_save_json = ask_save_json_data()
    is_save_excel = ask_save_excel_data()

    selected_time_scale_name = find_time_scale(time_scale)
    save_folder_name = f"{selected_time_scale_name}_scale_{start_version}_{end_version}"
    json_save_folder_path = os.path.join(json_save_folder_base_path, save_folder_name)
    excel_save_folder_base_path = os.path.join(current_dir, "scripts", "data", "timeData", dataType)
    excel_save_folder_path = os.path.join(excel_save_folder_base_path, save_folder_name)


    for path in Path(json_source_folder).glob("*.json"):
        data = load_json_data(path)
        file_name = path.stem
        if not file_name in version_detail.keys():
            continue
        if not is_in_version_range(file_name, start_version, end_version):
            continue

        print(f"data length: {len(data)}, file name: {file_name}")
        timed_data = convert_to_timed_data(data, initial_time, time_scale)
        save_json_data_conditionally(timed_data, os.path.join(json_save_folder_path, f"{file_name}.json"), is_save_json)
        save_excel_data_conditionally(timed_data, os.path.join(excel_save_folder_path, f"{file_name}.xlsx"), is_save_excel)


if __name__=="__main__":
    main()