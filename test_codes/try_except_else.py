def divide(x, y):
    try:
        result = x // y
    except ZeroDivisionError:
        print('Division Error occured')
        # print('Value of result is ', result)  # result cannot be accessed over here
    else:
        print('Value of division is ', result)  # result can be accessed over here.


if __name__ == '__main__':
    divide(45, 3)
    divide(54, 0)
