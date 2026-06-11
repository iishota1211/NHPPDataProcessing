from testModules.AbstractDataClass import AbstractDataClass

class TimeData(AbstractDataClass):

    __data : list

    def __init__(self,dataType,data):
        super().__init__(dataType)
        self.data = data

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self,data):
        print("setter is running")
        finalData = []
        for item in data:
            finalData.append(item+1)
        self.__data=finalData


    def printData(self):
        print(f"this class is {self.dataType}")
        for item in self.__data:
            print(item)

