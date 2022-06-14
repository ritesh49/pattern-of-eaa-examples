from table_module import TableModule, ProductType, DataSet


class Product(TableModule):
    def __init__(self, ds: DataSet):
        super(Product, self).__init__(ds, 'Products')

    def get_product_type(self, product_id: str) -> ProductType:
        type_code: str = self[product_id]['type']
        return ProductType[type_code]

    def __getitem__(self, key: str):
        _filter = {'_id': key}
        return self._table.select(_filter)
