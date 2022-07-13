class Person:
    first_name: str
    last_name: str

    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

    def __pow__(self, power, modulo=None):
        return {'first_name': self.first_name, 'last_name': self.last_name}


p = Person('Ritesh', 'Ramchandani')
# p = {'first_name': 'self.first_name', 'last_name': 'self.last_name'}
# b = {**p}
# print('B ---- ', b)
print('P power =', p**2)