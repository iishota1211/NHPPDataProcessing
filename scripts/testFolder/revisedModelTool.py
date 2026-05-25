from classicUtils import existSRM
from decimal import *
from numpy import emath

def logLikelihoodFunction(modelDict, dataType):
	modelType = modelDict["modelType"]
	likelihoodFun = None
	likelihoodFun_backup = None
	if modelType == "typeI":
		models = existSRM.ClassicTypeI()
		if dataType == "time":
			likelihoodFun = LLF_t_float
			likelihoodFun_backup = LLF_t
		if dataType == "group":
			likelihoodFun = LLF_g_float
			likelihoodFun_backup = LLF_g
	else:
		raise
	return likelihoodFun, likelihoodFun_backup


def LLF_t(args, timeDataFormat, meanValueFun, intensityFun):
    print(f"this is LLF_t")
    res = 0
    old_t = 0
    old_n = 0
    last_t,last_n, = timeDataFormat[-1]
    meanValue = meanValueFun(last_t, args)
    
    #print("last_t = "+str(last_t)+" args = "+str(args)+" meanValue = "+str(meanValue))
    
    #expMeanValue = Decimal(- meanValue).exp()
    #print("meanValue = "+str(meanValue)+" expMeanValue = "+str(expMeanValue))
    res = - meanValue
    i = 0
    for dataEle in timeDataFormat:
        t_i = dataEle[0]
        n_i = dataEle[1]
        intensity = intensityFun(t_i, args)
        if intensity == Decimal(0.0):
            return float("-inf")
        lnIntensity = Decimal(intensity).ln()
        #if i < 5:
        #i += 1
        res = res + lnIntensity
        #print("t_i = "+str(t_i)+" args = "+str(args)+" intensity = " + str(intensity)+" res = "+str(res))
        
    return float(res)

	# timeDataFormat[0] = [t_i, n_i]
	# t_i : failure time
	# n_i : cumulative number of software faults
def LLF_t_float(args, timeDataFormat, meanValueFun, intensityFun):
    print(f"this is LLF_t_float")
    res = 0
    old_t = 0
    old_n = 0
    last_t,last_n, = timeDataFormat[-1]
    try:
        meanValue = meanValueFun(last_t, args)
    except Exception as e:
        print(last_t)
        print(type(last_t))
        for x in args:
            print("x : "+str(x)+" type : "+str(type(x)))
        raise e
    
    #print("last_t : "+str(last_t)+" meanValue : "+str(meanValue))
    res = - meanValue
    i = 0
    for dataEle in timeDataFormat:
        t_i = dataEle[0]
        n_i = dataEle[1]
        intensity = intensityFun(t_i, args)
        try:
            if intensity == 0.0:
                return float("-inf")
            lnIntensity = emath.log(intensity)
        except Exception as e:
            print("args : "+str(args))
            print("i : "+str(i))
            print("t_i : "+str(t_i)+" intensity : "+str(intensity))
            raise e
        i += 1
        res = res + lnIntensity
    #print("res : ")
    #print("last_t : "+str(last_t)+" meanValue : "+str(meanValue)+" LLF : "+str(res))
    return float(res)


def LLF_g(args, groupDataFormat, meanValueFun, intensityFun):
		res = 0
		old_t = 0
		old_n = 0
		old_meanValue = Decimal(0)
		last_t = groupDataFormat[-1][0]
		res = - meanValueFun(last_t, args)
		#print(float(res))
		for dataEle in groupDataFormat:
			t_i = dataEle[0]
			n_i = dataEle[1]
			meanValue = meanValueFun(t_i, args)
			intervalMeanValue = meanValue - old_meanValue
			intervalN = n_i - old_n
			#print("interval N : "+str(intervalN))
			#print("intervalMeanValue = "+str(float(intervalMeanValue)))
			old_meanValue = meanValue
			old_n = n_i

			tempRes = Decimal(1)
			i = 1
			while i <= intervalN:
				tempRes = tempRes * (intervalMeanValue / Decimal(i))
				i += 1
			
			tempRes = tempRes.ln()
			#print("tempRes:"+str(float(tempRes)))
			res = res + tempRes

		return float(res)


	# t_i : calendar time
	# n_i : cumulative number of software faults
	# intensityFun is only used for matching parater to LLF_t, and is not used in LLF_g
def LLF_g_float(args, groupDataFormat, meanValueFun, intensityFun):
    res = 0
    old_t = 0
    old_n = 0
    old_meanValue = 0
    last_t = groupDataFormat[-1][0]
    res = - meanValueFun(last_t, args)
    #print(float(res))
    for dataEle in groupDataFormat:
        t_i = dataEle[0]
        n_i = dataEle[1]
        meanValue = meanValueFun(t_i, args)
        intervalMeanValue = meanValue - old_meanValue
        intervalN = n_i - old_n
        #print("interval N : "+str(intervalN))
        #print("intervalMeanValue = "+str(float(intervalMeanValue)))
        old_meanValue = meanValue
        old_n = n_i

        tempRes = 1
        i = 1
        while i <= intervalN:
            tempRes = tempRes * (intervalMeanValue / i)
            i += 1
        tempRes = emath.log(tempRes)
        #print("tempRes:"+str(float(tempRes)))
        res = res + tempRes

    return float(res)

def hello(string):
    print(f"hello: {string}")
    if(string == "func1"):
        return func1
    else:
        return func2

def func1(string):
    print(f"func1: {string}")

def func2(string):
    print(f"func2: {string}")