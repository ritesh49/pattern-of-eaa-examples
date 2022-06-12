import datetime
from typing import List

from revenue_revognition_problem.value_objects import Money, MfDate
from revenue_recognition import RevenueRecognition
from product import Product


class Contract:
    __revenue_recognitions: List[RevenueRecognition] = []
    __product: Product
    __revenue: Money
    __when_signed: MfDate
    __id: int

    def __init__(self, product: Product, revenue: Money, when_signed: MfDate):
        self.__product = product
        self.__revenue = revenue
        self.__when_signed = when_signed

    def recognized_revenue(self, as_of: datetime.datetime):
        result: Money = Money.dollars(0)

        for revenue_recognition in self.__revenue_recognitions:
            if revenue_recognition.is_recognizable_by(as_of=as_of):
                result = result.add(other=revenue_recognition.amount)

    def calculate_recognitions(self):
        self.__product.calculate_revenue_recognitions(self)

    def add_revenue_recognition(self, revenue_recognition: RevenueRecognition):
        pass

    @property
    def revenue(self):
        return self.__revenue

    @property
    def when_signed(self):
        return self.__when_signed
