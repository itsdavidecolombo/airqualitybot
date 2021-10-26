#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 19:11
# @Description: this script defines the classes that use database and sensor APIs.
#
#################################################
import builtins
from abc import ABC, abstractmethod
from airquality.api.url_querystring_builder import URLQuerystringBuilder
from airquality.parser.db_answer_parser import DatabaseAnswerParser
from airquality.database.sql_query_builder import SQLQueryBuilder
from airquality.database.db_conn_adapter import ConnectionAdapter
from airquality.api.api_request_adapter import APIRequestAdapter
from airquality.picker.api_packet_picker import APIPacketPicker
from airquality.parser.datetime_parser import DatetimeParser
from airquality.parser.file_parser import FileParserFactory
from airquality.app.session import Session
from airquality.app import EMPTY_STRING


class BaseBot(ABC):
    """Abstract Base Class for bot objects."""

    def __init__(self):
        self.__dbconn = None
        self.__sql_builder = None
        self.__api_adapter = None

    @property
    def sqlbuilder(self) -> SQLQueryBuilder:
        return self.__sql_builder

    @sqlbuilder.setter
    def sqlbuilder(self, value: SQLQueryBuilder):
        self.__sql_builder = value

    @property
    def dbconn(self) -> ConnectionAdapter:
        return self.__dbconn

    @dbconn.setter
    def dbconn(self, value: ConnectionAdapter):
        self.__dbconn = value

    @property
    def apiadapter(self) -> APIRequestAdapter:
        return self.__api_adapter

    @apiadapter.setter
    def apiadapter(self, value: APIRequestAdapter):
        self.__api_adapter = value

    @abstractmethod
    def run(self):
        pass

#############################################################################

#                           ATMOTUBE BOT                                    #

#############################################################################
class BotAtmotube(BaseBot):

    SENSOR_IDENTIFIER = "atmotube"

    def __init__(self):
        super().__init__()

    def run(self):

        if not self.apiadapter:
            raise SystemExit(f"{BotAtmotube.__name__}: missing api adapter.")

        if not self.dbconn:
            raise SystemExit(f"{BotAtmotube.__name__}: missing database connection adapter.")

        if not self.sqlbuilder:
            raise SystemExit(f"{BotAtmotube.__name__}: missing sql query builder.")

        for sensor_id in ids:


            # BUILD ATMOTUBE MEASURE PACKET FOR INSERTING DATA INTO TABLES
            packets = APIPacketPicker.reshape_atmotube_packets(
                    packets = parsed_api_answer["data"]["items"],
                    paramcode2paramid_map = id_code_dict,
                    last_timestamp = last_atmotube_timestamp
            )
            Session.get_current_session().debug_msg(f"{BotAtmotube.__name__}: try to pick API packets: OK")

            # TRY TO BUILD QUERY FOR INSERTING MEASUREMENT INTO DATABASE
            query = self.sqlbuilder.insert_atmotube_measurement_packets(packets)
            self.dbconn.send(query)
            Session.get_current_session().debug_msg(f"{BotAtmotube.__name__}: try to insert sensor measurements: OK")

            # UPDATE LAST TIMESTAMP FROM PACKETS
            last_timestamp = DatetimeParser.last_packet_timestamp(packets = packets)
            query = self.sqlbuilder.update_last_packet_date_atmotube(last_timestamp = last_timestamp, sensor_id = sensor_id)
            self.dbconn.send(query)
            Session.get_current_session().debug_msg(f"{BotAtmotube.__name__}: try to update last acquisition timestamp: OK")
