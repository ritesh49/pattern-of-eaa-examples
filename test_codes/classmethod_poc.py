class A:
    var1 = 10

    def __init__(self, param1: int):
        self.param = param1

    @classmethod
    def class_method(cls, param):
        print('var1 before class method -- ', cls.var1)
        cls.var1 = param  # only class variables can be accessed
        print('var1 after class method -- ', cls.var1)
        # print('Param after class method -- ', cls.param)
        return cls(param)

    @staticmethod
    def static_method(param):
        print('var1 before static method -- ', A.var1)
        A.var1 = param
        print('var1 after static method -- ', A.var1)
        return 1

    def method(self, param):
        print('Param in method before -- ', self.param)
        self.param = param
        print('Param in method after -- ', self.param)
        print('var1 in method before -- ', self.var1)
        self.var1 = param  # this doesn't updated var1 as it's class variable not instance variable
        print('var1 in method after -- ', self.var1)
        return 1


a = A(123)
A.class_method(523)
a.method(345)
a.static_method(234)

A.method(a, 982734)
A.class_method(2348)
A.static_method(237)

