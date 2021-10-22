#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 19:11
# @Description: this script defines the classes that use database and sensor APIs.
#
#################################################
import builtins
from abc import ABC, abstractmethod
from airquality.database.sql_query_builder import SQLQueryBuilder
from airquality.database.db_conn_adapter import ConnectionAdapter
from airquality.api.api_request_adapter import APIRequestAdapter


class BaseBot(ABC):
    """Abstract Base Class for bot objects."""

    def __init__(self):
        self.__sql_builder = None
        self.__dbconn = None
        self.__api_adapter = None

    @property
    def sqlbuilder(self):
        return self.__sql_builder

    @sqlbuilder.setter
    def sqlbuilder(self, value: SQLQueryBuilder):
        self.__sql_builder = value

    @property
    def dbconn(self):
        return self.__dbconn

    @dbconn.setter
    def dbconn(self, value: ConnectionAdapter):
        self.__dbconn = value

    @property
    def apiadapter(self):
        return self.__api_adapter

    @apiadapter.setter
    def apiadapter(self, value: APIRequestAdapter):
        self.__api_adapter = value

    @abstractmethod
    def run(self):
        pass


class BotAtmotube(BaseBot):

    def __init__(self):
        super().__init__()

    def run(self):

        if not self.apiadapter:
            raise SystemExit(f"{BotAtmotube.__name__}: missing api adapter.")

        if not self.dbconn:
            raise SystemExit(f"{BotAtmotube.__name__}: missing database connection adapter.")

        if not self.sqlbuilder:
            raise SystemExit(f"{BotAtmotube.__name__}: missing sql query builder.")



################################ FACTORY ################################
class BotFactory(builtins.object):


    @staticmethod
    def create_bot_from_personality(bot_personality: str) -> BaseBot:

        if bot_personality == "atmotube":
            return BotAtmotube()
        else:
            raise SystemExit(f"{BotFactory.__name__}: invalid bot personality {bot_personality}.")
