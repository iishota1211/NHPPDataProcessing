import math

from utility import *
import json

file_path = "results_by_version.json"
data = load_json_data(file_path)

edited_list = []
for DictInEachVersion in data:
    edited_dict = {}
    for modelName in DictInEachVersion:
        if modelName == "Pareto":
            pmse_list = DictInEachVersion[modelName]["PMSE"]
            aic_list = DictInEachVersion[modelName]["AIC"]
            for i in range(len(pmse_list)):
                edited_dict[f"{modelName}_c_{i}"] = {"PMSE": pmse_list[i], "AIC": aic_list[i]}
        else:
            edited_dict[modelName] = DictInEachVersion[modelName]
    edited_list.append(edited_dict)

sorted_list = []
for DictInEachVersion in edited_list:
    sorted_dict = DictInEachVersion.copy()
    for modelName in DictInEachVersion:
        sorted_dict = dict(sorted(sorted_dict.items(), key=lambda item: item[1]["PMSE"]))
    sorted_list.append(sorted_dict)

log_sorted_list = []
for DictInEachVersion in sorted_list:
    for modelName in DictInEachVersion:
        if DictInEachVersion[modelName]["PMSE"] > 0:
            DictInEachVersion[modelName]["PMSE"] = math.log(DictInEachVersion[modelName]["PMSE"])
    log_sorted_list.append(DictInEachVersion)
        


def saveResultsToFile(resultDict, filePath):
    with open(filePath, 'w') as f:
        json.dump(resultDict, f, indent=4)

saveResultsToFile(log_sorted_list, "sorted_results_by_log_PMSE.json")