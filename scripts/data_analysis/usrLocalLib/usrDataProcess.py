#from classicUtils import dataLoader
from revisedModules.classicUtils import dataLoader
import config

# 数据读取

# segmentPatternFlag : 时间数据的分割方式
# dataLength 为取前 x% 个数据点
# dataTime 为取最终测试时间的前 x% 的数据点
# normalFlag : 是否归一化处理时间数据
# None 为不归一化处理, int型数字为归一化为具体某值(通常为1000)
def loadData(segmentPatternFlag = "dataLength", normalFlag = None, timeDataSetList = config.timeDataSetList, groupDataSetList = config.groupDataSetList, predIntervalList = config.predIntervalList, sc = None):


	# 数据基础路径
	dataConfigDict = dict()
	
	if len(timeDataSetList) > 0:
		dataConfigDict["time"] = dict()
		dataConfigDict["time"]["path"] = config.baseTimeDataPath
		dataConfigDict["time"]["dataSet"] = timeDataSetList
	
	if len(groupDataSetList) > 0:
		dataConfigDict["group"] = dict()
		dataConfigDict["group"]["path"] = config.baseGroupDataPath
		dataConfigDict["group"]["dataSet"] = groupDataSetList

	for dataType in dataConfigDict:
		print(dataType)
		for dataName in dataConfigDict[dataType]["dataSet"]:
			print(dataName)

	# 读取数据
	dataSetDict = dataLoader.readData(dataConfigDict, predIntervalList, segmentPatternFlag, normalFlag)
	# 返回值结构
	# dataDict = dataSetDict[dataType][predInterval][dataName]
	# 训练数据
	# dataDict["culTrainData"]
	# dataDict["culFormatedTrainData"]
	# 测试数据
	# dataDict["culTestData"]
	# dataDict["culFormatedTestData"]
	# 用于统一数据长度. 所有的外部输入 t 都要乘以 dataLengthCoe 以后再参与计算
	# 目的是统一时间数据的长度，便于选取推参初始值
	# 验证通过dataLoader加载的数据集时已自动处理，无需额外修改代码
	# dataDict["dataLengthCoe"]

	return dataSetDict



	