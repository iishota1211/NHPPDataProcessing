from classicUtils import SRMtool, readExcel
import copy,os

def readData(dataConfigDict, predIntervalList, segmentPatternFlag = "dataLength", normalFlag = None):
	# 数据集
	dataSetDict = dict()
	dataTypeList = ["time", "group"]
	# 读取数据
	for dataType in dataConfigDict:
		if dataType not in dataTypeList:
			print("coreInit.readData() : "+str(dataType)+" 类型的数据不存在")
			raise
		dataSetDict[dataType] = dict()
		dataPath = dataConfigDict[dataType]["path"]

		# 读取数据
		
		dataDict = dict()
		for dataName in dataConfigDict[dataType]["dataSet"]:
			#print("1."+dataType + dataName)
			tempDict = dict()
			fileName = dataName + ".xlsx"
			filePath = os.path.join(dataPath, fileName)
			wb = readExcel.WorkBook(filePath)
			sheetLength = wb.getSheetLength()
			counter = 0
			i = 0
			while i < sheetLength:
				tempList = wb.getCol(i, 0)
				sheetName = wb.getSheetName(i)
				dataList = []
				for ele in tempList:
					if ele != "":
						dataList.append(float(ele))
				
				if len(dataList) != 0:
					tempDict[sheetName] = dataList
					counter += 1
				i += 1
			#print("counter : "+str(counter))
			if counter == 1:
				for sheetName in tempDict:
					#print("1.1."+dataName.replace("/",""))
					dataDict[dataName.replace("/","")] = tempDict[sheetName]
			elif counter > 1:
				for sheetName in tempDict:
					#print("1.2."+dataName.replace("/",""))
					dataDict[sheetName.replace("/","")] = tempDict[sheetName]

		
		# 组装和处理数据
		
		#for dataName in dataConfigDict[dataType]["dataSet"]:
		#	fileName = dataPath + dataName + ".xlsx"
		#	dataList = SRMtool.readXlsxData(fileName)
		#	dataName = dataName.replace("/","")
		
		#haveZeroDataList = []
		#notZeroDataList = []

		for dataName in dataDict:
			#print("2."+dataType + dataName)
			dataList = dataDict[dataName]
			dataSetDict[dataType][dataName] = dict()
			for predInterval in predIntervalList:
				if predInterval > 1.0:
					tempInterval = 1.0
				else:
					tempInterval = predInterval
				# 取前 x% 个数据点
				if dataType == "group" or segmentPatternFlag == "dataLength":
					culTrainData, culTestData = SRMtool.cutPercentageData(dataList,tempInterval,"round")
				# 取最终测试时间的前 x% 的数据点 (仅限时间数据)
				elif segmentPatternFlag == "dataTime":
					endTime = tempInterval * dataList[-1]
					culTrainData = []
					culTestData = []
					for nowTime in dataList:
						if nowTime <= endTime:
							culTrainData.append(nowTime)
						else:
							culTestData.append(nowTime)
				dataSetDict[dataType][dataName][predInterval] = dict()
				# 用于统一数据长度. 所有的输入 t 都要乘以 dataLengthCoe 以后再参与计算
				# 根据实验结果, 统一数据长度后多数情况可以得到一样的估计结果
				# 但是少数情况下会导致性能恶化。如非必要尽量不开启
				# 使用python原生的最大似然估计时建议开启，否则无法配合推荐初始值。
				# 某种意义来说, 统一（缩短）数据长度也许类似于降低估计精度。
				# 让原本不可行的数值计算变得可行。但是精度会降低可能会导致预测性能下降。
				if dataType == "time":
					if normalFlag is not None:
						#normalFlag = 1000
						dataLengthCoe = normalFlag / culTrainData[-1]
					else:
						dataLengthCoe = 1
				elif dataType == "group":
					dataLengthCoe = 1
				dataSetDict[dataType][dataName][predInterval]["dataLengthCoe"] = dataLengthCoe
				t_trainData = copy.deepcopy(culTrainData)
				t_testData = copy.deepcopy(culTestData)
				culTrainData = [x * dataLengthCoe for x in t_trainData]
				culTestData = [x * dataLengthCoe for x in t_testData]

				"""
				# 提示数据问题
				if predInterval == predIntervalList[-1]:
					tempNonCulList = SRMtool.toNonCulData(culTrainData)
					if 0 in tempNonCulList:
						haveZeroDataList.append(dataType+" "+dataName)
					else:
						notZeroDataList.append(dataType+" "+dataName)
				"""
				
				dataSetDict[dataType][dataName][predInterval]["culTrainData"] = culTrainData
				dataSetDict[dataType][dataName][predInterval]["culTestData"] = culTestData
				
				if dataType == "group":
					culFormatedTrainData = SRMtool.toFormatGroupData(culTrainData)
					culFormatedTestData = SRMtool.toFormatGroupData(culTestData, len(culTrainData) + 1 )
				elif dataType == "time":
					culFormatedTrainData = SRMtool.toFormatTimeData(culTrainData)
					culFormatedTestData = SRMtool.toFormatTimeData(culTestData, len(culTrainData) + 1 )
				# 补充0数据
				if predInterval > 1.0:
					endTime = culFormatedTrainData[-1][0]
					endNum = culFormatedTrainData[-1][1]
					futureTime = round(endTime * predInterval)
					culFormatedTrainData.append([futureTime,endNum])
				dataSetDict[dataType][dataName][predInterval]["culFormatedTrainData"] = culFormatedTrainData
				dataSetDict[dataType][dataName][predInterval]["culFormatedTestData"] = culFormatedTestData

	"""
	print("----------- 以下数据含有0数据 -----------")
	for haveZeroData in haveZeroDataList:
		print(haveZeroData)
	print("----------- 以下数据不含有0数据 ---------")
	for notZeroData in notZeroDataList:
		print(notZeroData)
	print("----------------------------------------")
	"""

	# v02 调换 dataName 与 predInterval 在字典中的顺序
	newDataSetDict = dict()
	for dataType in dataConfigDict:
		newDataSetDict[dataType] = dict()
		for predInterval in predIntervalList:
			newDataSetDict[dataType][predInterval] = dict()
			for dataName in dataSetDict[dataType]:
				#print(dataType + dataName)
				dataName = dataName.replace("/","")
				newDataSetDict[dataType][predInterval][dataName] = dict()
				newDataSetDict[dataType][predInterval][dataName]["culTrainData"]			= dataSetDict[dataType][dataName][predInterval]["culTrainData"]
				newDataSetDict[dataType][predInterval][dataName]["culTestData"]				= dataSetDict[dataType][dataName][predInterval]["culTestData"]
				newDataSetDict[dataType][predInterval][dataName]["culFormatedTrainData"]	= dataSetDict[dataType][dataName][predInterval]["culFormatedTrainData"]
				newDataSetDict[dataType][predInterval][dataName]["culFormatedTestData"]		= dataSetDict[dataType][dataName][predInterval]["culFormatedTestData"]

	return newDataSetDict