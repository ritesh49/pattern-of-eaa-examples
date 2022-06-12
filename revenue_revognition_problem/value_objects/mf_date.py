import datetime


class MfDate:
    __mf_date: datetime.datetime

    def __init__(self, mf_date: datetime.datetime):
        self.__mf_date = mf_date

    def add_days(self, days: int):
        return MfDate(self.__mf_date + datetime.timedelta(days=days))
    
    @property
    def value(self):
        return self.__mf_date
