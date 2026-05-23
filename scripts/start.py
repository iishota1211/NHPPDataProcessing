# cd /Users/kuretakahase/GoogleDrive/学术代码v0.1/单线程版计算框架/
# python3 start.py

# 注意：使用时需要在终端里进入当前目录，否则报找不到文件夹错误


from usrLocalLib import usrDataProcess, usrReportProcess
from classicGlobalLib import classicEM
from classicUtils import modelTool
import config

# supports 14 Type-I NHPP models:
#modelNameList 	= ["Exp","Gamma","Pareto","TruncNormal","LogNormal","TruncLogist","LogLogist","TruncEVMax","LogEVMax","TruncEVMin","LogEVMin","Log","Plaw","Gtlogist"]
# calculation for Log,Plaw,Gtlogist models is unstable. Exluding them is recommended for now.
modelNameList 	= ["Exp","Gamma","Pareto","TruncNormal","LogNormal","TruncLogist","LogLogist","TruncEVMax","LogEVMax","TruncEVMin","LogEVMin"]

print("获取数据")
# 标准化数据读取
dataSetDict = usrDataProcess.loadData(config.segmentPatternFlag, config.normalFlag)
#人工检验数据正确性
usrReportProcess.saveDataReport(dataSetDict)


print("Executing program")
for dataType in dataSetDict:
	for predInterval in dataSetDict[dataType]:
		for dataName in dataSetDict[dataType][predInterval]:
			# Get a single data dictionary
			# (data type = dataType, dataset split phase = predInterval, dataset name = dataName)
			print(f"dataType : {dataType}, dataName : {dataName}, predInterval : {predInterval}")
			dataDict = dataSetDict[dataType][predInterval][dataName]
			# Standard format of the data dictionary
			# Standard formatted training data
			culFormatedTrainData = dataDict["culFormatedTrainData"]
			print("normalized training data")
			for nowTime, nowNum in culFormatedTrainData:
				print(f"(Time) {nowTime} : (Actual Value) {nowNum}")
			# normalized test data / predition data
			culFormatedTestData = dataDict["culFormatedTestData"]
			print("normalized test data")
			for nowTime, nowNum in culFormatedTestData:
				print(f"(Time) {nowTime} : (Actual Value) {nowNum}")

			modelType = "typeI"
			AICs = []
			print(f"Start parameter estimation for data: {dataName}")
			for modelName in modelNameList:
				# declare modeDict for storing model name and model type
				modelDict = dict()
				modelDict["modelType"] = modelType
				modelDict["modelName"] = modelName

				# model inplementation
				meanValueFun, meanValueFun_backup = modelTool.meanValueFunction(modelDict)
				intensityFun, intensityFun_backup = modelTool.intensityFunction(modelDict)
				likelihoodFun, likelihoodFun_backup = modelTool.logLikelihoodFunction(modelDict, dataType)
				parameterBounds = modelTool.parameterBounds(modelDict)

				#  Default is None, this parameter is not actually used
				methodDict = None
				# start parameter estimation
				resDict = classicEM.parameterEstimate(methodDict, modelDict, dataType, culFormatedTrainData)
				paraList = resDict["paraList"]
				AICs.append(resDict["measureValueDict"]["AIC"])
				print(f"Model: {modelName}")
				print(f"paramter List: {paraList}")
				print(f"Measure Names: {resDict['measureNameList']}")
				print(f"Measure Values: {resDict['measureValueDict']['AIC']}")

				# printing prediction values
				for nowTime, nowNum in culFormatedTestData:
					predNum = meanValueFun(nowTime, paraList)
					print(f"(Time) {nowTime} : (Predicted Value) {predNum}")
				print("\n")
				
			for modelName, AIC in zip(modelNameList, AICs):
				print(f"Model: {modelName}, AIC: {AIC}")



print("program finished")




















