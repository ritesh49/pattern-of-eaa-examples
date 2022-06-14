from decimal import Decimal
from typing import List

from table_module import TableModule, DataSet, DataRow, ProductType
from revenue_recognition import RevenueRecogntion
from product import Product


class Contract(TableModule):
    """
        New dataset can be created of contract module using
        contract = Contract(dataset)
    """

    def __init__(self, ds: DataSet):
        super(Contract, self).__init__(ds, 'Contracts')

    def calculate_recognitions(self, contract_id: str):
        contract_row: DataRow = self[contract_id]
        amount: Decimal = contract_row['amount']
        rr: RevenueRecogntion = RevenueRecogntion(self._table.dataset)
        prod: Product = Product(self._table.dataset)
        prod_id = self.get_product_id(contract_id)

        if prod.get_product_type(prod_id) == ProductType.WP:
            rr.insert(contract_id, amount, self.get_when_signed(contract_id))

        elif prod.get_product_type(prod_id) == ProductType.SS:
            allocation: List[Decimal] = self.allocate(amount, 3)
            rr.insert(contract_id, allocation[0], self.get_when_signed(contract_id))
            rr.insert(contract_id, allocation[1], self.get_when_signed(contract_id).add_days(60))
            rr.insert(contract_id, allocation[2], self.get_when_signed(contract_id).add_days(90))

        elif prod.get_product_type(prod_id) == ProductType.DB:
            allocation: List[Decimal] = self.allocate(amount, 3)
            rr.insert(contract_id, allocation[0], self.get_when_signed(contract_id))
            rr.insert(contract_id, allocation[1], self.get_when_signed(contract_id).add_days(30))
            rr.insert(contract_id, allocation[2], self.get_when_signed(contract_id).add_days(60))

        else:
            raise Exception('Invalid product id')

    @staticmethod
    def allocate(amount: Decimal, by: int) -> List[Decimal]:
        low_result: Decimal = amount / by
        low_result = Decimal.__round__(low_result, 2)
        high_result = low_result + Decimal(0.01)
        results: List[Decimal] = [Decimal() for _ in range(by)]
        remainder: int = int(amount / by)
        for i in range(remainder):
            results[i] = high_result
        for i in range(remainder, by):
            results[i] = low_result
        return results

    def __getitem__(self, key: str):
        _filter = {'_id': key}
        return self._table.select(_filter)
