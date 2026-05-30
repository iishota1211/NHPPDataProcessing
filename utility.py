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

def append_data(dict,key,value):
    if key in dict:
        dict[key].append(value)
    else:
        dict[key] = [value]
    return dict

def save_to_excel(list, file_path):
    df = pd.DataFrame(list)
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    
    with pd.ExcelWriter(file_path) as writer:
        df.to_excel(writer, index=False, header=False)