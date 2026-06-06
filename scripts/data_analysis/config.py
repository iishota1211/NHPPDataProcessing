from conf import dataInfo
from pathlib import Path
import time, os

timeDataSetList = dataInfo.timeDataSetList_CSS_small
groupDataSetList 	= dataInfo.groupDataSetList_CSS_TR_small
predIntervalList 	= [0.5, 1.0]
parent_dir_path = os.path.dirname(os.path.realpath(__file__))
folderName = os.path.basename(parent_dir_path)

# True parameters of the simulated dataset
trueParaDict = dataInfo.trueParaDict

nowTime = str(time.strftime('%Y_%m%d_%H%M_%S_', time.localtime(time.time())))

# Time data segmentation method:
# Use the first x% of data points (dataLength)
# or use the data points within the first x% of the final test time (dataTime)
segmentPatternFlag = "dataLength"

# Whether to normalize the time data
# None = no normalization
# Integer value = normalize to that specific value (typically 1000)
normalFlag = None

dictUniName = folderName

projectType = ""
prefixStr 	= ""
whlPath 	= ""
currentRoot 	= parent_dir_path

dataRoot = os.path.join(currentRoot, "data")
reportPath = os.path.join(currentRoot, "report")
loadPath = os.path.join(dataRoot, "tempVarSave")
savePath = os.path.join(dataRoot, "tempVarSave")
dataPersistencePath = os.path.join(reportPath,projectType + "_" + nowTime[0:-1])
baseGroupDataPath 	= os.path.join(dataRoot, "groupData")
baseTimeDataPath 	= os.path.join(dataRoot, "timeData")


for path_name, path in {
    "dataRoot": dataRoot,
    "reportPath": reportPath,
    "dataPersistencePath": dataPersistencePath,
}.items():
    p = Path(path)

    if not p.exists():
        p.mkdir(parents=True, exist_ok=True)
        print(f"Created directory {path_name}")
    else:
        print(f"Directory {path_name} already exists")