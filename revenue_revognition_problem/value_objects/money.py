class Money:
    amount: float

    def __init__(self, amount, currency: str = 'dollars'):
        if isinstance(amount, float) or isinstance(amount, int):
            self.amount = amount
        elif isinstance(amount, Money):
            self.amount = amount.amount
        else:
            raise Exception('Expecting int or float or Money type instance for amount')
        self._curr = currency

    @classmethod
    def dollars(cls, amount: float):
        cls.amount = amount
        return cls(amount)


    @classmethod
    def allocate(cls, no: int):
        return [Money.dollars(i) for i in [cls.amount/no] * no]

    def add(self, other):
        if isinstance(other, Money):
            return self.amount + other.amount
        else:
            raise Exception('Expecting Money type instance for addition or money')

    def multiple(self, other):
        if isinstance(other, Money):
            return self.amount * other.amount
        raise Exception('Expecting Money type instance for multiple or money')
