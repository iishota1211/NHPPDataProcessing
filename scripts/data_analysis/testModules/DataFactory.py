from testModules.TimeDataClass import TimeData
from testModules.GroupDataClass import GroupData

class DataFactory:

    @staticmethod
    def create(data_type, data):

        if data_type == "time":
            return TimeData(data_type, data)

        if data_type == "group":
            return GroupData(data_type, data)

        raise ValueError(f"Unknown data type: {data_type}")