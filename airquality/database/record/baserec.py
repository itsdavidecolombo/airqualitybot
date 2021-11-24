######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 05/11/21 17:37
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.api2db.baseunif as baseunif
import airquality.database.datatype.timestamp as ts


class ParamIDTimestamp:

    def __init__(self, sensor_id: int, timestamp: ts.Timestamp):
        self.id = sensor_id
        self.timestamp = timestamp


class BaseRecord:
    pass


class BaseRecordBuilder(abc.ABC):

    @abc.abstractmethod
    def record(self, sensor_data: baseunif.BaseUniformResponse, sensor_id: int) -> BaseRecord:
        pass
