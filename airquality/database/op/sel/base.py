######################################################
#
# Author: Davide Colombo
# Date: 24/11/21 14:26
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Dict
import airquality.database.op.baseop as baseop
import airquality.database.conn.adapt as db
import airquality.database.util.query as query
import airquality.types.channel as chtype
import airquality.types.timestamp as ts


class ParamNameID:

    def __init__(self, id_: int, name: str):
        self.id = id_
        self.name = name


################################ SELECT WRAPPER ################################
class SelectWrapper(baseop.DatabaseWrapper, abc.ABC):

    def __init__(self, conn: db.DatabaseAdapter, builder: query.QueryBuilder, sensor_type: str, log_filename="log"):
        super(SelectWrapper, self).__init__(conn=conn, builder=builder, log_filename=log_filename)
        self.sensor_type = sensor_type

    @abc.abstractmethod
    def select(self):
        pass

    def _select_api_param(self, sensor_id: int) -> List[chtype.Channel]:
        api_param = []
        api_param_query = self.query_builder.select_api_param_from_sensor_id(sensor_id=sensor_id)
        api_param_resp = self.database_conn.send(api_param_query)
        for ch_key, ch_id, ch_name, last_acquisition in api_param_resp:

            last_acquisition_timestamp = ts.from_database_timestamp_to_timestamp(database_timestamp=last_acquisition)

            api_param.append(
                chtype.Channel(ch_id=ch_id, ch_key=ch_key, ch_name=ch_name, last_acquisition=last_acquisition_timestamp)
            )
        return api_param

    def select_max_sensor_id(self) -> int:
        sel_query = self.query_builder.select_max_sensor_id()
        response = self.database_conn.send(sel_query)
        max_id = response[0][0]
        return 1 if max_id is None else (max_id+1)

    def select_measure_param(self) -> Dict[str, int]:
        name2id = {}
        meas_param_query = self.query_builder.select_measure_param_from_sensor_type(sensor_type=self.sensor_type)
        measure_param_resp = self.database_conn.send(meas_param_query)
        for param_code, param_id in measure_param_resp:
            name2id[param_code] = param_id
        return name2id
