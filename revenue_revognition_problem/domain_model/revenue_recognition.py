import datetime

from revenue_revognition_problem.value_objects.money import Money


class RevenueRecognition:
    __amount: Money
    __mf_date: datetime.datetime

    def __init__(self, amount: Money, mf_date: datetime.datetime):
        self.__amount = amount
        self.__mf_date = mf_date

    @property
    def amount(self) -> Money:
        return Money(self.__amount)

    def is_recognizable_by(self, as_of: datetime.datetime):
        return as_of >= self.__mf_date
