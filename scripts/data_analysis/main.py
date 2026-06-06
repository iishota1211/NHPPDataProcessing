import json
import os
from classicUtils import modelTool
from testFolder import revisedModelTool
from usrLocalLib import usrDataProcess
from classicGlobalLib import classicEM
import config
from test_functions import *
import matplotlib.pyplot as plt
import numpy as np

modelNameList 	= ["Exp","Gamma","Pareto","LogEVMin","Plaw","Log"]
modelNameList 	= ["Exp","Pareto","Plaw","Log"]

model_with_parameter_c_list = ["Gamma","Pareto","LogEVMin"]
dataSetDict = usrDataProcess.loadData(config.segmentPatternFlag, config.normalFlag)
modelType = "typeI"
dataType = "time"
predInterval = 0.5

def testLLF(methodDict, modelDict, dataType, dataDict):
    meanValueFun, meanValueFun_backup = modelTool.meanValueFunction(modelDict)
    culFormatedTrainData = dataDict["culFormatedTrainData"]
    resDict = classicEM.parameterEstimate(methodDict, modelDict, dataType, culFormatedTrainData)
    paraList = resDict["paraList"]
    culFormatedTestData = dataDict["culFormatedTestData"]
    AIC = resDict["measureValueDict"]["AIC"]
    modelName = modelDict["modelName"]
    print(f"Model: {modelName}")
    print(f"parameter List: {paraList}")
    print(f"Measure Names: {resDict['measureNameList']}")
    print(f"Measure Values: {resDict['measureValueDict']['AIC']}")

    predList = []
    actualList = []
    for nowTime, nowNum in culFormatedTestData:
        predNum = meanValueFun(nowTime, paraList)
        predList.append(predNum)
        actualList.append(nowNum)
        print(f"(Time) {nowTime} : (Predicted Value) {predNum}")
    print("\n")

    pmse = calculatePMSE(culFormatedTestData, meanValueFun, paraList)
    print(f"PMSE: {pmse}")

    resultDict = dict()
    resultDict["AIC"] = AIC
    resultDict["PMSE"] = pmse

    return resultDict

def mergeDataSet(dataSetDict):
    lastDataName = list(dataSetDict[dataType][predInterval].keys())[-1]

    FinalFormatedTrainData = []
    FinalFormatedTestData = []
    for dataName in dataSetDict[dataType][predInterval]:
        culFormatedTrainData = dataSetDict[dataType][predInterval][dataName]["culFormatedTrainData"]
        culFormatedTestData = dataSetDict[dataType][predInterval][dataName]["culFormatedTestData"]

        mergedFormatedData = culFormatedTrainData + culFormatedTestData
        if dataName != lastDataName:
            FinalFormatedTrainData = FinalFormatedTrainData + mergedFormatedData
        else:
            FinalFormatedTestData = FinalFormatedTestData + mergedFormatedData

    return FinalFormatedTrainData, FinalFormatedTestData

def mergeDataSetByVersion(dataSetDict):
    lastDataName = list(dataSetDict[dataType][predInterval].keys())[-1]

    FinalFormatedTrainDataList = []
    FinalFormatedTestData = []
    CurrentTotalValue = 0
    for dataName in dataSetDict[dataType][predInterval]:
        culFormatedTrainData = dataSetDict[dataType][predInterval][dataName]["culFormatedTrainData"]
        culFormatedTestData = dataSetDict[dataType][predInterval][dataName]["culFormatedTestData"]

        mergedFormatedData = culFormatedTrainData + culFormatedTestData
        if dataName != lastDataName:
            FinalMergedFormatedData = addExtraValueToDataset(mergedFormatedData, CurrentTotalValue)
            CurrentTotalValue = FinalMergedFormatedData[-1][1]
            FinalFormatedTrainDataList.append(FinalMergedFormatedData)
        else:
            FinalMergedFormatedData = addExtraValueToDataset(mergedFormatedData, CurrentTotalValue)
            FinalFormatedTestData = FinalMergedFormatedData

    return FinalFormatedTrainDataList, FinalFormatedTestData

def addExtraValueToDataset(dataSet, extraValue):
    newDataSet = []
    for nowTime, nowNum in dataSet:
        newDataSet.append((nowTime, nowNum + extraValue))
    return newDataSet

def calculatePMSE(culFormatedTestData, meanValueFun, paraList):
    predList = []
    actualList = []
    
    for nowTime, nowNum in culFormatedTestData:
        predNum = meanValueFun(nowTime, paraList)
        predList.append(predNum)
        actualList.append(nowNum)

    if len(predList) != len(actualList):
        raise ValueError("Length of predicted list and actual list must be the same.")
    
    mse = sum((pred - actual) ** 2 for pred, actual in zip(predList, actualList)) / len(predList)
    return mse

def displayDifference(culFormatedTestData, meanValueFun, paraList):
    for nowTime, nowNum in culFormatedTestData:
        predNum = meanValueFun(nowTime, paraList)
        print(f"(Time) {nowTime} : (Predicted Value) {predNum}, (Actual Value) {nowNum}, (Difference) {predNum - nowNum}")

def displayTrainDataSets(culFormatedTrainDataList):
    for culFormatedTrainData in culFormatedTrainDataList:
        for nowTime, nowNum in culFormatedTrainData:
            print(f"(Time) {nowTime} : (Actual Value) {nowNum}")

def displayTestDataSet(culFormatedTestData):
    for nowTime, nowNum in culFormatedTestData:
        print(f"(Time) {nowTime} : (Actual Value) {nowNum}")

def saveResultsToFile(resultDict, filePath):
    with open(filePath, 'w') as f:
        json.dump(resultDict, f, indent=4)

def sliceDataSetDictByVersion(dataSetDict,startVersion, endVersion):
    dataSetByVersionDict = dataSetDict
    for key in list(dataSetDict[dataType][predInterval].keys()):
        dataName = key
        version = int(dataName.split("_")[-1])
        if version < startVersion or version > endVersion:
            dataSetByVersionDict[dataType][predInterval].pop(dataName)
    return dataSetByVersionDict

def displayFigure(function,data,paraList):
    initial_x = data[0][0]
    final_x = data[-1][0]
    x = np.linspace(initial_x, final_x, 100)
    plt.plot(x, function(x, paraList), label='Data',linestyle='',marker='o', color='blue')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Multiple Lines Plot')
    plt.legend()
    # plt.savefig(os.path.join("results", "multiple_lines_plot.png"))
    plt.show()


firstVersionNum = 30
lastVersionNum = 35
totalVersionNum = lastVersionNum - firstVersionNum + 1
resultList = []

for i in range(totalVersionNum-1):
    resultDictByDataSetNum = dict()
    dataSetDict = sliceDataSetDictByVersion(dataSetDict, firstVersionNum + i, lastVersionNum)
    print("dataset after slicing by version:")
    for dataName in dataSetDict[dataType][predInterval]:
        print(f"dataName: {dataName}")


    culFormatedTrainDataList, culFormatedTestData = mergeDataSetByVersion(dataSetDict)

    for modelName in modelNameList:
        modelDict = dict()
        modelDict["modelType"] = modelType
        modelDict["modelName"] = modelName
        methodDict = None
        meanValueFun, meanValueFun_backup = modelTool.meanValueFunction(modelDict)

        paraList_scipy, aic = calculate_parameters(modelDict, dataType, culFormatedTrainDataList)
        pmse = []
        if paraList_scipy is None:
            print(f"Model {modelName} does not support parameter estimation yet.")
        elif modelName in model_with_parameter_c_list:
            for para in paraList_scipy:
                pmse.append(calculatePMSE(culFormatedTestData, meanValueFun, para))
                print(f"PMSE for model {modelName} with parameters {para}: {pmse[-1]}\n")
                print(f"AIC for model {modelName}: {aic}\n")
        else:
            pmse = calculatePMSE(culFormatedTestData, meanValueFun, paraList_scipy)
            print(f"PMSE for model {modelName} with parameters {paraList_scipy}: {pmse}\n")
            print(f"AIC for model {modelName}: {aic}\n")

        resultDictByDataSetNum[modelName] = {"PMSE": pmse, "AIC": aic}
    resultList.append(resultDictByDataSetNum)
    meanValueFunLog = modelTool.meanValueFunction({"modelType": modelType, "modelName": "Log"})[0]
    displayFigure(meanValueFunLog, culFormatedTestData, paraList_scipy)

# saveResultsToFile(resultList, "results_by_version.json")
for i in range(totalVersionNum-1):
    print(f"final result for version range {firstVersionNum + i} - { lastVersionNum}:")
    for modelName in resultList[i]:
        print(f"Model: {modelName}, PMSE: {resultList[i][modelName]['PMSE']}, AIC: {resultList[i][modelName]['AIC']}")
    print("\n")