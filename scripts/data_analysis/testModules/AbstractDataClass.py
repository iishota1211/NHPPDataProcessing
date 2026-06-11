from abc import ABC, abstractmethod


class AbstractDataClass(ABC):

    dataType = None

    def __init__(self, dataType:str):
        self.dataType = dataType

    @abstractmethod
    def printData(self):
        pass

