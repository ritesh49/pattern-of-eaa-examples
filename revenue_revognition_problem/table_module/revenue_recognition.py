import datetime
from decimal import Decimal

from table_module import TableModule, DataSet


class RevenueRecogntion(TableModule):
    def __init__(self, ds: DataSet):
        super(RevenueRecogntion, self).__init__(ds, 'RevenueRecognitions')

    def insert(self, contract_id: int, amount: Decimal, date: datetime.datetime):
        new_row = self._table.new_row()
        id = self.get_next_id()
        new_row['id'] = id
        new_row['contract_id'] = contract_id
        new_row['amount'] = amount
        new_row['date'] = date
        self._table.rows.add(new_row)
        return id

    def recognized_revenue(self, contract_id: int, as_of: datetime.datetime):
        _filter = {'contract_id': contract_id, 'date': {'$lte': as_of}}
        compute_expression = 'sum(amount)'
        _sum = self._table.compute(compute_expression, _filter)
        return 0 if _sum is None else Decimal(_sum)
