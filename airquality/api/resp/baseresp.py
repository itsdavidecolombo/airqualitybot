######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:39
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Dict, Any, List


class BaseResponse(abc.ABC):
    pass


class ParamNameValue:

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value


class BaseResponseBuilder(abc.ABC):

    def __init__(self, api_response_class=BaseResponse):
        self.api_response_class = api_response_class

    @abc.abstractmethod
    def build(self, parsed_response: Dict[str, Any]) -> List[BaseResponse]:
        pass
