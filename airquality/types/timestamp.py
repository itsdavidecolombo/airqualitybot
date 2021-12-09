#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 12:04
# @Description: this script defines a class for parsing sensor's API timestamps
#
#################################################
import abc
import datetime as dt

THINGSPK_FMT = "%Y-%m-%dT%H:%M:%SZ"
ATMOTUBE_FMT = "%Y-%m-%dT%H:%M:%S.000Z"
SQL_TIMEST_FMT = "%Y-%m-%d %H:%M:%S"


################################ TIMESTAMP CLASS ################################
class Timestamp(abc.ABC):

    def __init__(self, timest: str, fmt: str = SQL_TIMEST_FMT):
        self._ts = timest
        self.fmt = fmt

    @property
    def ts(self) -> str:
        my_dt = dt.datetime.strptime(self._ts, self.fmt)
        return my_dt.strftime(SQL_TIMEST_FMT)

    @abc.abstractmethod
    def add_days(self, days: int):
        pass

    @abc.abstractmethod
    def is_after(self, other) -> bool:
        pass


################################ SQL TIMESTAMP CLASS ################################
class SQLTimestamp(Timestamp):

    def __init__(self, timest: str, fmt: str = SQL_TIMEST_FMT):
        super(SQLTimestamp, self).__init__(timest=timest, fmt=fmt)

    def add_days(self, days: int) -> Timestamp:
        my_dt = dt.datetime.strptime(self._ts, self.fmt)
        my_dt = my_dt + dt.timedelta(days=days)
        return SQLTimestamp(my_dt.strftime(SQL_TIMEST_FMT), SQL_TIMEST_FMT)

    def is_after(self, other) -> bool:
        if not isinstance(other, SQLTimestamp) or isinstance(other, NullTimestamp):
            raise SystemExit(f"{SQLTimestamp.__name__}: bad type => cannot compare with object of type='{other.__class__.__name__}'")

        self_dt = dt.datetime.strptime(self._ts, self.fmt)
        other_dt = dt.datetime.strptime(other._ts, other.fmt)
        return (self_dt - other_dt).total_seconds() > 0

    def is_same_day(self, other) -> bool:
        if not isinstance(other, SQLTimestamp) or isinstance(other, NullTimestamp):
            raise SystemExit(f"{SQLTimestamp.__name__}: bad type => cannot compare with object of type='{other.__class__.__name__}'")

        self_dt = dt.datetime.strptime(self._ts, self.fmt).date()
        other_dt = dt.datetime.strptime(other._ts, other.fmt).date()
        return self_dt.__eq__(other_dt)


################################ ATMOTUBE TIMESTAMP CLASS ################################
class AtmotubeTimestamp(SQLTimestamp):

    def __init__(self, timest: str, fmt: str = ATMOTUBE_FMT):
        super(AtmotubeTimestamp, self).__init__(timest=dt.datetime.strptime(timest, fmt).strftime(SQL_TIMEST_FMT))

    def add_days(self, days: int = 1) -> Timestamp:
        return super().add_days(days)

    def is_after(self, other) -> bool:
        return super().is_after(other)
    
    def is_same_day(self, other) -> bool:
        return super(AtmotubeTimestamp, self).is_same_day(other)


################################ THINGSPEAK TIMESTAMP CLASS ################################
class ThingspeakTimestamp(SQLTimestamp):

    def __init__(self, timest: str, fmt: str = THINGSPK_FMT):
        super(ThingspeakTimestamp, self).__init__(timest=dt.datetime.strptime(timest, fmt).strftime(SQL_TIMEST_FMT))

    def add_days(self, days: int = 7) -> Timestamp:
        return super().add_days(days)

    def is_after(self, other) -> bool:
        return super().is_after(other)

    def is_same_day(self, other) -> bool:
        return super(ThingspeakTimestamp, self).is_same_day(other)


################################ CURRENT TIMESTAMP CLASS ################################
class CurrentTimestamp(SQLTimestamp):

    def __init__(self):
        super(CurrentTimestamp, self).__init__(timest=dt.datetime.now().strftime(SQL_TIMEST_FMT), fmt=SQL_TIMEST_FMT)

    def add_days(self, days: int) -> Timestamp:
        return super().add_days(days)

    def is_after(self, other):
        return super().is_after(other)

    def is_same_day(self, other) -> bool:
        return super(CurrentTimestamp, self).is_same_day(other)


################################ UNIX TIMESTAMP CLASS ################################
class UnixTimestamp(SQLTimestamp):

    def __init__(self, timest: int, fmt: str = SQL_TIMEST_FMT):
        super(UnixTimestamp, self).__init__(timest=dt.datetime.fromtimestamp(timest).strftime(SQL_TIMEST_FMT), fmt=fmt)

    def add_days(self, days: int) -> Timestamp:
        return super().add_days(days)

    def is_after(self, other) -> bool:
        return super().is_after(other)

    def is_same_day(self, other) -> bool:
        return super(UnixTimestamp, self).is_same_day(other)


################################ NULL TIMESTAMP CLASS ################################
class NullTimestamp(SQLTimestamp):

    def __init__(self, timest="NULL"):
        super(NullTimestamp, self).__init__(timest=dt.datetime.now().strftime(SQL_TIMEST_FMT), fmt=SQL_TIMEST_FMT)
        self._ts = timest

    @property
    def ts(self) -> str:
        return self._ts

    def is_after(self, other) -> bool:
        raise SystemExit(f"{NullTimestamp.__name__}: not implemented")

    def add_days(self, days: int):
        raise SystemExit(f"{NullTimestamp.__name__}: not implemented")


################################ USEFUL CONVERSION METHOD ################################

def datetime2timestamp(datetime_: dt.datetime) -> SQLTimestamp:
    return SQLTimestamp(timest=datetime_.strftime(SQL_TIMEST_FMT), fmt=SQL_TIMEST_FMT)
