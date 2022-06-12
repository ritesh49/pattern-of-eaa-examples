import datetime

from revenue_revognition_problem.value_objects import Money, MfDate
from revenue_revognition_problem.transaction_script.mongodb import DatabaseClient as conn, MONGO_DATABASE

REVENUE_RECOGNITIONS_COLLECTION = 'revenue_recognitions'


class Gateway:
    def __init__(self):
        self._db = conn()[MONGO_DATABASE][REVENUE_RECOGNITIONS_COLLECTION]

    def find_recognitions_for(self, contract_id: int, as_of: MfDate):
        yield self._db.find({'contract': contract_id, 'recognized_on': {'$lte': as_of.value}})

    def find_contract(self, contract_id: int):
        return self._db.find_one({'contract': contract_id})

    def insert_recognition(self, contract_id: int, amount: Money, as_of: MfDate):
        return self._db.insert({'contract': contract_id, 'amount': amount, 'as_of': as_of.value})
