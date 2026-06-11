from testModules.AbstractDataClass import AbstractDataClass

class GroupData(AbstractDataClass):

    data: list

    def __init__(self,dataType,data):
        super().__init__(dataType)
        self.data=data

    def printData(self):
        print(f"this class is {self.dataType}")
        for item in self.data:
            print(item)