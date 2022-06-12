from abc import ABCMeta, abstractmethod
from typing import List

from revenue_revognition_problem.value_objects import Money
from revenue_recognition import RevenueRecognition
from contract import Contract


class RecognitionStrategy(metaclass=ABCMeta):

    @abstractmethod
    def calculate_revenue_recognitions(self, contract: Contract):
        pass


class CompleteRecognitionStrategy(RecognitionStrategy):
    def calculate_revenue_recognitions(self, contract: Contract):
        contract.add_revenue_recognition(RevenueRecognition(contract.revenue, contract.when_signed))


class ThreeWayRecognitionStrategy(RecognitionStrategy):
    __first_recognition_offset: int
    __second_recognition_offset: int

    def __init__(self, first_recognition_offset: int, second_recognition_offset: int):
        self.__first_recognition_offset = first_recognition_offset
        self.__second_recognition_offset = second_recognition_offset

    def calculate_revenue_recognitions(self, contract: Contract):
        allocation: List[Money] = contract.revenue.allocate(3)
        contract.add_revenue_recognition(RevenueRecognition(allocation[0], contract.when_signed))
        contract.add_revenue_recognition(
            RevenueRecognition(allocation[1], contract.when_signed.add_days(self.__first_recognition_offset)))
        contract.add_revenue_recognition(
            RevenueRecognition(allocation[2], contract.when_signed.add_days(self.__second_recognition_offset)))
