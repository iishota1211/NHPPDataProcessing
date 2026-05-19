import zipfile
from pathlib import Path
import os 

current_dir = os.path.dirname(os.path.realpath(__file__))
source_folder_name = "json"
source_file_name = "nvdcve-2.0-2026.json"
source_dir = os.path.join(current_dir, source_folder_name, source_file_name)

