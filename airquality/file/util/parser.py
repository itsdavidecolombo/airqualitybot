#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 10:24
# @Description: this script defines the classes for parsing file content from different extensions.
#
#################################################
import abc
import json
from typing import Dict, Any
import airquality.logger.loggable as log
import airquality.logger.util.decorator as log_decorator


def get_file_parser(file_fmt: str, log_filename="log"):

    if file_fmt == 'json':
        return JSONParser(log_filename=log_filename)
    else:
        raise SystemExit(f"'{get_file_parser.__name__}()': bad file format='{file_fmt}' => supported format are: [ JSON ]")


class FileParser(log.Loggable):

    def __init__(self, log_filename="log"):
        super(FileParser, self).__init__(log_filename=log_filename)

    @abc.abstractmethod
    def parse(self, text: str) -> Dict[str, Any]:
        pass


class JSONParser(FileParser):

    def __init__(self, log_filename="log"):
        super(JSONParser, self).__init__(log_filename=log_filename)

    @log_decorator.log_decorator()
    def parse(self, text: str) -> Dict[str, Any]:
        try:
            return json.loads(text)
        except json.decoder.JSONDecodeError as je:
            raise SystemExit(f"{JSONParser.__name__}: bad json schema => {je!s}")
