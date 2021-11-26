######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 11:54
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List
import airquality.api2db.adptype as adptype
import airquality.api.resp.resp as resp


class APIRespAdapt(abc.ABC):

    @abc.abstractmethod
    def adapt(self, api_resp: List[resp.APIRESPTYPE]) -> List[adptype.ADPTYPE]:
        pass