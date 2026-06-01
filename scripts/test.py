import json
import os
from classicUtils import modelTool
from testFolder import revisedModelTool
from usrLocalLib import usrDataProcess
from classicGlobalLib import classicEM
import config
from test_functions import *

modelNameList 	= ["Exp","Gamma","Pareto","LogEVMin","Plaw","Log"]
modelNameList 	= ["Exp","Pareto","Plaw","Log"]

model_with_parameter_c_list = ["Gamma","Pareto","LogEVMin"]
dataSetDict = usrDataProcess.loadData(config.segmentPatternFlag, config.normalFlag)
modelType = "typeI"
dataType = "time"

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


for predInterval in dataSetDict[dataType]:

    culFormatedTrainDataList, culFormatedTestData = mergeDataSetByVersion(dataSetDict)

    for modelName in modelNameList:
        modelDict = dict()
        modelDict["modelType"] = modelType
        modelDict["modelName"] = modelName
        methodDict = None
        meanValueFun, meanValueFun_backup = modelTool.meanValueFunction(modelDict)
    
        print(f"Testing model: {modelName}")
        paraList_scipy = calculate_parameters(modelDict, dataType, culFormatedTrainDataList)
        pmse = []
        if paraList_scipy is None:
            print(f"Model {modelName} does not support parameter estimation yet.")
        elif modelName in model_with_parameter_c_list:
            for para in paraList_scipy:
                pmse.append(calculatePMSE(culFormatedTestData, meanValueFun, para))
                print(f"PMSE for model {modelName} with parameters {para}: {pmse[-1]}\n")
        else:
            pmse = calculatePMSE(culFormatedTestData, meanValueFun, paraList_scipy)
            print(f"PMSE for model {modelName} with parameters {paraList_scipy}: {pmse}\n")