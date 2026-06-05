import math
from testFolder import revisedModelTool
from usrLocalLib import usrDataProcess, usrReportProcess
from classicGlobalLib import classicEM
from classicUtils import modelTool
import config
from scipy import optimize

modelNameList 	= ["Exp","Gamma","Pareto","LogEVMin","Plaw","Log"]
model_with_parameter_c_list = ["Gamma","Pareto","LogEVMin"]

def exp(last_t,last_n):
    a = 2*last_n
    b = math.log(2) / last_t
    return [a,b]

def gamma(last_t,last_n):
    pass

def pareto(last_t,last_n):
    a = 2 * last_n
    a_list = [a,a]
    b_list = []
    c_list = [0.1, 10]

    for c in c_list:
        partA = math.log(2)
        partB = math.log(last_t + c) - math.log(c)
        res = partA / partB
        b_list.append(res)

    return [a_list, b_list, c_list]

def logEVMin(last_t,last_n):
    a = 2 * last_n
    a_list = [a,a]
    b_list = []
    c_list = [0.1, 10]

    for c in c_list:
        partA = c + math.log(last_t)
        partB = math.log(math.log(2))
        res = partA / partB
        b_list.append(res)

    return [a_list, b_list, c_list]

def powerLaw(last_t,last_n):
    a = 2 * last_n
    b = - math.log(2) / math.log(last_t)
    return [a,b]

def log_poisson(last_t,last_n):
    a = 2 * last_n
    
    partA = math.sqrt(math.e)-1
    partB = math.log(last_t)
    b = partA / partB

    return [a,b]

model_without_parameter_c_dict = {
    "Exp": exp,
    "Plaw": powerLaw,
    "Log": log_poisson
}

model_with_parameter_c_dict = {
    "Pareto": pareto,
    "LogEVMin": logEVMin
}

def guess_init_parameters(trainData,modelDict):
    last_t,last_n, = trainData[-1]
    modelName = modelDict["modelName"]
    if modelName in model_with_parameter_c_list:
        parameter_func = model_with_parameter_c_dict.get(modelName)
        parameters = parameter_func(last_t, last_n) if parameter_func else None
        return parameters
    else:
        parameter_func = model_without_parameter_c_dict.get(modelDict["modelName"])
        parameters = parameter_func(last_t, last_n) if parameter_func else None
        return parameters

def calculate_parameters(modelDict, dataType, culFormatedTrainDataList):
    meanValueFun, meanValueFun_backup = modelTool.meanValueFunction(modelDict)
    intensityFun, intensityFun_backup = modelTool.intensityFunction(modelDict)
    likelihoodFun, likelihoodFun_backup = revisedModelTool.logLikelihoodFunction(modelDict, dataType)
    likelihoodFunMultiversion = likelihoodFun_backup
    parameterBounds = modelTool.parameterBounds(modelDict)

    if likelihoodFun is None:
        print(f"Model {modelDict['modelName']} does not support parameter estimation yet.")
        return None

    def lossFun(paraList, culFormatedTrainData, meanValueFun, intensityFun):
        return -likelihoodFunMultiversion(paraList, culFormatedTrainData, meanValueFun, intensityFun)
    
    initPara = guess_init_parameters(culFormatedTrainDataList[-1], modelDict)
    if initPara is None:
        print(f"Model {modelDict['modelName']} does not support parameter estimation yet.")
        return None
    
    print("calculating parameters for model: "+modelDict["modelName"]+" with initial parameters: "+str(initPara))
    if len(initPara) == 2:
        optimizeRes = optimize.minimize(lossFun, initPara, args=(culFormatedTrainDataList, meanValueFun, intensityFun), bounds=parameterBounds)
        paraList = optimizeRes.x
        aic = optimizeRes.fun*2 + 2*len(initPara)

        return paraList,aic
    elif len(initPara) == 3:
        a_list, b_list, c_list = initPara
        paraList = []
        aic = []
        for i in range(len(c_list)):
            a = a_list[i]
            b = b_list[i]
            c = c_list[i]
            optimizeRes = optimize.minimize(lossFun, [a, b, c], args=(culFormatedTrainDataList, meanValueFun, intensityFun), bounds=parameterBounds)
            paraList.append(optimizeRes.x)
            aic.append(optimizeRes.fun*2 + 2*len(initPara))
            #print(f"Parameters for model {modelDict['modelName']} with c={c}: {paraList[-1]}")

        return paraList,aic
    else:
        return None
    
def test_parameters(parameterList, modelDict, dataType, culFormatedTrainData):
    meanValueFun, meanValueFun_backup = modelTool.meanValueFunction(modelDict)
    intensityFun, intensityFun_backup = modelTool.intensityFunction(modelDict)
    likelihoodFun, likelihoodFun_backup = revisedModelTool.logLikelihoodFunction(modelDict, dataType)

    if likelihoodFun is None:
        print(f"Model {modelDict['modelName']} does not support parameter estimation yet.")
        return None

    def lossFun(paraList, culFormatedTrainData, meanValueFun, intensityFun):
        return -likelihoodFun(paraList, culFormatedTrainData, meanValueFun, intensityFun)
    
    optimizeRes = optimize.minimize(lossFun, parameterList, args=(culFormatedTrainData, meanValueFun, intensityFun), bounds=modelTool.parameterBounds(modelDict))
    paraList = optimizeRes.x

    return paraList

def main():
    dataSetDict = usrDataProcess.loadData(config.segmentPatternFlag, config.normalFlag)
    dataType = "time"
    predInterval = 0.5
    dataName = "DS1"
    dataDict = dataSetDict[dataType][predInterval][dataName]

    print(f"dataType : {dataType}, dataName : {dataName}, predInterval : {predInterval}")
    dataDict = dataSetDict[dataType][predInterval][dataName]
    culFormatedTrainData = dataDict["culFormatedTrainData"]

    print("normalized training data")
    for nowTime, nowNum in culFormatedTrainData:
        print(f"(Time) {nowTime} : (Actual Value) {nowNum}")

    culFormatedTestData = dataDict["culFormatedTestData"]
    print("normalized test data")
    for nowTime, nowNum in culFormatedTestData:
        print(f"(Time) {nowTime} : (Actual Value) {nowNum}")

    modelType = "typeI"
    AICs = []
    for modelName in modelNameList:
        # declare modeDict for storing model name and model type
        modelDict = dict()
        modelDict["modelType"] = modelType
        modelDict["modelName"] = modelName

        # model inplementation
        meanValueFun, meanValueFun_backup = modelTool.meanValueFunction(modelDict)
        intensityFun, intensityFun_backup = modelTool.intensityFunction(modelDict)
        parameterBounds = modelTool.parameterBounds(modelDict)

        methodDict = None
        # start parameter estimation
        resDict = classicEM.parameterEstimate(methodDict, modelDict, dataType, culFormatedTrainData)
        paraList = resDict["paraList"]

        paraList_scipy, aic = test_parameters(paraList, modelDict, dataType, culFormatedTrainData)
        AICs.append(resDict["measureValueDict"]["AIC"])
        print(f"Model: {modelName}")
        print(f"original paramter List: {paraList}")
        if paraList_scipy is not None:
            print(f"Scipy paramter List: {paraList_scipy}")
        print(f"Measure Names: {resDict['measureNameList']}")
        print(f"Measure Values: {resDict['measureValueDict']['AIC']}")

        # printing prediction values
        for nowTime, nowNum in culFormatedTestData:
            predNum = meanValueFun(nowTime, paraList)
            print(f"(Time) {nowTime} : (Predicted Value) {predNum}")
        print("\n")
    
    for modelName, AIC in zip(modelNameList, AICs):
        print(f"Model: {modelName}, AIC: {AIC}")

if __name__ == "__main__":
    main()
