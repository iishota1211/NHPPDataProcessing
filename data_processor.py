import os
import json

current_dir = os.path.dirname(os.path.realpath(__file__))

source_folder_name = "json"
source_folder = os.path.join(current_dir, source_folder_name)
source_file_name = "nvdcve-2.0-2026.json"
source_dir = os.path.join(current_dir, source_folder_name, source_file_name)

with open(source_dir, 'r', encoding='utf-8') as f:
    data = json.load(f)
    vulnerabilities = data.get("vulnerabilities", [])
    cves = [vulnerability.get("cve") for vulnerability in vulnerabilities]
    filtered_cves = []
    for cve in cves:
        published = cve.get("published")
        