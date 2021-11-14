#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 10:29
# @Description: this script defines a class for dynamically build valid sql queries. The query are read from the
#               'properties/query.json' file.
#
#################################################
from typing import List
import airquality.database.util.sql.record as rec
import airquality.file.structured.json as struct


class QueryBuilder:

    def __init__(self, query_file: struct.JSONFile):
        self.query_file = query_file

    ################################ METHODS THAT RETURN SELECT QUERY STATEMENT ################################
    def select_max_sensor_id(self) -> str:
        return self.query_file.s1

    def select_api_param_from_sensor_id(self, sensor_id) -> str:
        return self.query_file.s2.format(sensor_id=sensor_id)

    def select_sensor_ids_from_sensor_type(self, sensor_type: str) -> str:
        return self.query_file.s3.format(personality=sensor_type)

    def select_sensor_names_from_sensor_type(self, sensor_type: str) -> str:
        return self.query_file.s4.format(personality=sensor_type)

    def select_measure_param_from_sensor_type(self, sensor_type: str) -> str:
        return self.query_file.s5.format(personality=sensor_type)

    def select_active_locations(self, sensor_type: str) -> str:
        return self.query_file.s6.format(personality=sensor_type)

    def select_sensor_name_id_mapping_from_sensor_type(self, sensor_type: str) -> str:
        return self.query_file.s7.format(personality=sensor_type)

    def select_last_acquisition(self, channel: str, sensor_id: int):
        return self.query_file.s8.format(sensor_id=sensor_id, channel=channel)

    ################################ METHODS THAT RETURN INSERT INTO QUERY STATEMENT ################################

    def insert_into_mobile_measurements(self) -> str:
        return self.query_file.i1

    def insert_into_station_measurements(self) -> str:
        return self.query_file.i2

    def update_locations(self, values: List[rec.LocationRecord]) -> str:
        query = ""
        for value in values:
            query += self.query_file.u2.format(ts=value.valid_from, sens_id=value.sensor_id)
        query += self.__insert_location_values(values)
        return query

    def initialize_sensors(self,
                           sensor_values: List[rec.SensorRecord],
                           api_param_values: List[rec.APIParamRecord],
                           location_values: List[rec.LocationRecord],
                           sensor_info_values: List[rec.SensorInfoRecord]):
        query = self.__insert_into_sensor(sensor_values)
        query += self.__insert_into_api_param(api_param_values)
        query += self.__insert_location_values(location_values)
        query += self.__insert_sensor_info_values(sensor_info_values)
        return query

    ################################ PRIVATE METHODS ################################
    def __insert_into_sensor(self, values: List[rec.SensorRecord]) -> str:
        query = self.query_file.i3
        for value in values:
            query += value.record() + ','
        return query.strip(',') + ';'

    def __insert_into_api_param(self, values: List[rec.APIParamRecord]) -> str:
        query = self.query_file.i4
        for value in values:
            query += value.record() + ','
        return query.strip(',') + ';'

    def __insert_location_values(self, values: List[rec.LocationRecord]) -> str:
        query = self.query_file.i5
        for value in values:
            query += value.record() + ','
        return query.strip(',') + ';'

    def __insert_sensor_info_values(self, values: List[rec.SensorInfoRecord]) -> str:
        query = self.query_file.i6
        for value in values:
            query += value.record() + ','
        return query.strip(',') + ';'
