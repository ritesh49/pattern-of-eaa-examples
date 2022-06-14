from enum import Enum, unique


@unique
class ProductType(Enum):
    WW = 'WW'
    BB = 'BB'


if __name__ == '__main__':
    ww = ProductType['WW']
    print(type(ww))  # returns ProductType
    print(ww)  # returns ProductType.WW
    print(ProductType.WW == 'abc')  # returns False
    print(ProductType['hasd'])  # throws KeyError
