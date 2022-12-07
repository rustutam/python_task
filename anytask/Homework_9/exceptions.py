#!/usr/bin/env python

import sys


def f0():
    return int('abc')


def f1():
    import rus


def f2():
    return 19.3 ** 100000


def f3():
    raise FloatingPointError


def f4():
    return 19.3 ** 100000


def f5():
    return 1 / 0


def f6():
    assert 1 == "1"


def f7():
    class Human:
        male = "men"
        age = 19
    h1 = Human
    return h1.weight


def f8():
    open("abc.txt", 'r')


def f9():
    import sur


def f10():
    a = [1, 2, 3, 4]

    return a[6]


def f11():
    a = [1, 2, 3, 4]

    return a[5]


def f12():
    a = {1: '1',
            2: '2',
            3: '3',
            4: '4'}

    return a[5]


def f13():
    return name


def f14():
    eval('a === a')


def f15():
    return int('abc')


def f16():
    'питон'.encode('ascii')


def check_exception(f, exception):
    try:
        f()
    except exception:
        pass
    else:
        print("Bad luck, no exception caught: %s" % exception)
        sys.exit(1)


check_exception(f0, BaseException)
check_exception(f1, Exception)
check_exception(f2, ArithmeticError)
check_exception(f3, FloatingPointError)
check_exception(f4, OverflowError)
check_exception(f5, ZeroDivisionError)
check_exception(f6, AssertionError)
check_exception(f7, AttributeError)
check_exception(f8, EnvironmentError)
check_exception(f9, ImportError)
check_exception(f10, LookupError)
check_exception(f11, IndexError)
check_exception(f12, KeyError)
check_exception(f13, NameError)
check_exception(f14, SyntaxError)
check_exception(f15, ValueError)
check_exception(f16, UnicodeError)

print("Congratulations, you made it!")
