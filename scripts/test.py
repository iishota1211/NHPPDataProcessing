import json
import os
from classicUtils import modelTool
from testFolder import revisedModelTool
from usrLocalLib import usrDataProcess
from classicGlobalLib import classicEM
import config
from test_functions import *

modelNameList 	= ["Exp","Gamma","Pareto","LogEVMin","Plaw","Log"]
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
    print(f"paramter List: {paraList}")
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

    pmse = calculatePMSE(predList, actualList)
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
    for dataName in dataSetDict[dataType][predInterval]:
        culFormatedTrainData = dataSetDict[dataType][predInterval][dataName]["culFormatedTrainData"]
        culFormatedTestData = dataSetDict[dataType][predInterval][dataName]["culFormatedTestData"]

        mergedFormatedData = culFormatedTrainData + culFormatedTestData
        if dataName != lastDataName:
            FinalFormatedTrainDataList.append(mergedFormatedData)
        else:
            FinalFormatedTestData = mergedFormatedData

    return FinalFormatedTrainDataList, FinalFormatedTestData

def calculatePMSE(predList, actualList):
    if len(predList) != len(actualList):
        raise ValueError("Length of predicted list and actual list must be the same.")
    
    mse = sum((pred - actual) ** 2 for pred, actual in zip(predList, actualList)) / len(predList)
    return mse


for predInterval in dataSetDict[dataType]:

    culFormatedTrainDataList, culFormatedTestData = mergeDataSetByVersion(dataSetDict)
    lastCulFormatedTrainData = culFormatedTrainDataList[-1]

    for modelName in modelNameList:
        modelDict = dict()
        modelDict["modelType"] = modelType
        modelDict["modelName"] = modelName
        methodDict = None
    
        print(f"Testing model: {modelName}")
        paraList_scipy = calculate_parameters(modelDict, dataType, culFormatedTrainDataList)
        print(f"Estimated parameters for model {modelName} using scipy.optimize: {paraList_scipy}")
    #     resultDict = testLLF(methodDict, modelDict, dataType, DataDict)
    #     resultList.append((modelName, resultDict))

    # for modelName, resultDict in resultList:
    #     print(f"Model: {modelName}, AIC: {resultDict['AIC']}, PMSE: {resultDict['PMSE']}")