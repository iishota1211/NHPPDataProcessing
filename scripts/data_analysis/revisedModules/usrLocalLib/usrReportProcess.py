import config
from classicLocalLib import classicReportProcess

# 保存数据报告
def saveDataReport(dataSetDict):
	classicReportProcess.saveBaseDataSet(dataSetDict, config.dataPersistencePath, config.prefixStr)