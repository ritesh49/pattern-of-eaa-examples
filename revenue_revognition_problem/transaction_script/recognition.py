from gateway import Gateway
from revenue_revognition_problem.value_objects import Money, MfDate

SPREADSHEET = 'S'
WORDPROCESSOR = 'W'
DATABASE = 'D'


class RecognitionService:
    def __init__(self):
        self.db = Gateway()

    def recognized_revenue(self, contract_number: int, mf_date: MfDate) -> Money:
        result: Money = Money.dollars(0)
        try:
            result_set = self.db.find_recognitions_for(contract_number, mf_date)
            while next(result_set):
                result = result.add(Money.dollars(result_set.big_decimal('amount')))
            return result
        except:
            raise Exception('Error in recognized_revenue function')

    def calculate_revenue_recognitions(self, contract_number: int):
        contract = self.db.find_contract(contract_number)
        total_revenue = Money.dollars(contract['revenue'])
        recognition_date: MfDate = contract['date_signed']
        contract_type = contract['type']

        if contract_type == SPREADSHEET:
            allocation: list = total_revenue.allocate(3)
            self.db.insert_recognition(contract_number, allocation[0], recognition_date)
            self.db.insert_recognition(contract_number, allocation[1], recognition_date.add_days(60))
            self.db.insert_recognition(contract_number, allocation[2], recognition_date.add_days(90))

        elif contract_type == WORDPROCESSOR:
            self.db.insert_recognition(contract_number, total_revenue, recognition_date)

        elif contract_type == DATABASE:
            allocation: list = total_revenue.allocate(3)
            self.db.insert_recognition(contract_number, allocation[0], recognition_date)
            self.db.insert_recognition(contract_number, allocation[1], recognition_date.add_days(30))
            self.db.insert_recognition(contract_number, allocation[2], recognition_date.add_days(60))
