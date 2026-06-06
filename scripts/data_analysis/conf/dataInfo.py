# 和数据有关的配置仓库。包括用得上的和用不上的配置。其余 config 文件所需的数据信息全部从这里统一引用 
#
# 可引用对象 : 
# 
# timeDataSetList_SIM 				模拟数据 100组 	exp模型
# timeDataSetList_SIM_small 		模拟数据 2组	 	exp模型
# 
# timeDataSetList_CSS 				闭源软件时间数据 	8组
# timeDataSetList_CSS_small 		闭源软件时间数据 	1组
# 
# timeDataSetList_OSS_8set 			开源软件时间数据 	8组
# timeDataSetList_OSS_8set_small 	开源软件时间数据 	1组
# timeDataSetList_OSS_8set_type2	开源软件时间数据 	8组
# timeDataSetList_OSS_all 			开源软件时间数据 	101组
# timeDataSetList_OSS_all_small 	开源软件时间数据 	2组
# 
# 
# groupDataSetList_CSS_type1 		闭源软件组数据 	8组 组合1
# groupDataSetList_CSS_type2 		闭源软件组数据 	8组 组合2
# 
# groupDataSetList_OSS_8set 		开源软件组数据 	8组
# groupDataSetList_OSS_8set_small 	开源软件组数据 	1组
# groupDataSetList_OSS_all 			开源软件组数据 	若干组 (百来组)


############## 时间数据 数据集配置 ##############

# SIM
timeDataSetList_SIM 				= ["simulationData",]
timeDataSetList_SIM_small 			= ["simulationData_small",]

timeDataSetList_Exp1000 			= ["Exp_SimData_b1000",]
timeDataSetList_Gamma1000 			= ["Gamma_SimData_b1000",]
timeDataSetList_Pareto1000 			= ["Pareto_SimData_b1000",]
timeDataSetList_TruncNormal1000 	= ["TruncNormal_SimData_b1000",]
timeDataSetList_LogNormal1000 		= ["LogNormal_SimData_b1000",]
timeDataSetList_TruncLogist1000 	= ["TruncLogist_SimData_b1000",]
timeDataSetList_LogLogist1000 		= ["LogLogist_SimData_b1000",]
timeDataSetList_TruncEVMax1000 		= ["TruncEVMax_SimData_b1000",]
timeDataSetList_LogEVMax1000 		= ["LogEVMax_SimData_b1000",]
timeDataSetList_TruncEVMin1000 		= ["TruncEVMin_SimData_b1000",]
timeDataSetList_LogEVMin1000 		= ["LogEVMin_SimData_b1000",]

timeDataSetList_Exp100 				= ["Exp_SimData_b100_standard",]
timeDataSetList_Gamma100 			= ["Gamma_SimData_b100_standard",]
timeDataSetList_Pareto100 			= ["Pareto_SimData_b100_standard",]
timeDataSetList_TruncNormal100 		= ["TruncNormal_SimData_b100_standard",]
timeDataSetList_LogNormal100 		= ["LogNormal_SimData_b100_standard",]
timeDataSetList_TruncLogist100 		= ["TruncLogist_SimData_b100_standard",]
timeDataSetList_LogLogist100 		= ["LogLogist_SimData_b100_standard",]
timeDataSetList_TruncEVMax100 		= ["TruncEVMax_SimData_b100_standard",]
timeDataSetList_LogEVMax100 		= ["LogEVMax_SimData_b100_standard",]
timeDataSetList_TruncEVMin100 		= ["TruncEVMin_SimData_b100_standard",]
timeDataSetList_LogEVMin100 		= ["LogEVMin_SimData_b100_standard",]

trueParaDict = dict()
trueParaDict["Exp"] = [150, 0.00004]
trueParaDict["Gamma"] = [160, 1, 0.00002]
trueParaDict["Pareto"] = [1000, 0.05, 5000]
trueParaDict["TruncNormal"] = [150, 80000, -200000]
trueParaDict["LogNormal"] = [500, 0.8, 10]
trueParaDict["TruncLogist"] = [150, 30000, -100000]
trueParaDict["LogLogist"] = [250, 0.5, 10]
trueParaDict["TruncEVMax"] = [150, 30000, -100000]
trueParaDict["LogEVMax"] = [200, 1, 10]
trueParaDict["TruncEVMin"] = [150, 230000, 500000]
trueParaDict["LogEVMin"] = [200, 1, -10]


# CSS
timeDataSetList_CSS 				= ["DS1","DS2","DS3","DS4","DS5","DS6","DS7","DS8"]
timeDataSetList_CSS_small 			= ["DS1",]
timeDataSetList_CSS_TR				= ["TR/DS1","TR/DS2","TR/DS3","TR/DS4","TR/DS5","TR/DS6","TR/DS7","TR/DS8"]

# OSS
timeDataSetList_OSS_8set 			= ["github/tabler","github/astro","github/notable","github/caffe","github/MonitorControl","github/bootstrap","github/hexo","github/HTTPieCil"]
timeDataSetList_OSS_8set_small 		= ["github/tabler",]
timeDataSetList_OSS_8set_type2 		= ["github/notable","github/openzeppelin-contracts","github/spleeter","github/k3s","github/pytorch-image-models","github/httpie","github/nest","github/go",]
timeDataSetList_OSS_all 			= ["github_issues_cleanedTimeData",]
timeDataSetList_OSS_all_small 		= ["github_issues_cleanedTimeData_small",]

############## 组数据 数据集配置 ##############

# CSS
groupDataSetList_CSS_type1 			= ["DS1","DS2","DS3","DS4","haarGroupData/DS2","DS6","DS7","haarGroupData/DS4"]
groupDataSetList_CSS_type2 			= ["DS1","DS2","DS3","Lyu/J1","Lyu/J3","DS6","Lyu/J5","Lyu/SS1"]
groupDataSetList_CSS_TR 			= ["DS1","DS2","DS3","DS4","DS5","DS6","DS7","DS8"]
groupDataSetList_CSS_TR_small 		= ["DS1",]

# OSS
groupDataSetList_OSS_8set 			= ["github/zig","github/ccxt","github/styled-components","github/netty","github/vue","github/angular","github/redis","github/xstate"]
groupDataSetList_OSS_8set_small 	= ["github/zig","github/ccxt"]
groupDataSetList_OSS_all 			= ["github_issues_cleanedGroupData",]