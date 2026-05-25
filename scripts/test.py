import math

from classicUtils import modelTool
from testFolder import revisedModelTool
from usrLocalLib import usrDataProcess
from classicGlobalLib import classicEM
import config

modelNameList 	= ["Exp","Gamma","Pareto","TruncNormal","LogNormal","TruncLogist","LogLogist","TruncEVMax","LogEVMax","TruncEVMin","LogEVMin"]
dataSetDict = usrDataProcess.loadData(config.segmentPatternFlag, config.normalFlag)
modelType = "typeI"
dataType = "time"
args = [0.1, 0.2, 0.3]


for dataType in dataSetDict:
    for predInterval in dataSetDict[dataType]:
        for dataName in dataSetDict[dataType][predInterval]:
            print(f"dataType : {dataType}, dataName : {dataName}, predInterval : {predInterval}")
            dataDict = dataSetDict[dataType][predInterval][dataName]
            culFormatedTrainData = dataDict["culFormatedTrainData"]
            for nowTime, nowNum in culFormatedTrainData:
                print(f"(Time) {nowTime} : (Actual Value) {nowNum}")
            culFormatedTestData = dataDict["culFormatedTestData"]
            for modelName in modelNameList:
                modelDict = dict()
                modelDict["modelType"] = modelType
                modelDict["modelName"] = modelName
                methodDict = None

                meanValueFun, meanValueFun_backup = modelTool.meanValueFunction(modelDict)
                intensityFun, intensityFun_backup = modelTool.intensityFunction(modelDict)
                likelihoodFun, likelihoodFun_backup = revisedModelTool.logLikelihoodFunction(modelDict, dataType)

                resDict = classicEM.parameterEstimate(methodDict, modelDict, dataType, culFormatedTrainData)
                paraList = resDict["paraList"]
                if not meanValueFun or not intensityFun or not likelihoodFun:
                    print(f"Model {modelName} is not implemented yet.")
                    break
                print(f"Log-likelihood function value for model {modelName} : {likelihoodFun(paraList, culFormatedTrainData, meanValueFun, intensityFun)}")