from recognition_strategy import RecognitionStrategy, CompleteRecognitionStrategy, ThreeWayRecognitionStrategy
from contract import Contract


class Product:
    __name: str
    __recognition_strategy: RecognitionStrategy

    def __init__(self, name: str, recognition_strategy: RecognitionStrategy):
        self.__name = name
        self.__recognition_strategy = recognition_strategy

    def calculate_revenue_recognitions(self, contract: Contract):
        self.__recognition_strategy.calculate_revenue_recognitions(contract)

    @staticmethod
    def new_word_processor(name):
        return Product(name, CompleteRecognitionStrategy())

    @staticmethod
    def new_spreadsheet(name):
        return Product(name, ThreeWayRecognitionStrategy(60, 90))

    @staticmethod
    def new_database(name):
        return Product(name, ThreeWayRecognitionStrategy(30, 60))
