#!/usr/bin/env python3

import unittest
import re
import datetime
from collections import OrderedDict


def merge(*iterables, key=None):
    """
    Функция склеивает упорядоченные по ключу `key` и порядку «меньше»
    коллекции из `iterables`.
    Результат — итератор на упорядоченные данные.
    В случае равенства данных следует их упорядочить в порядке следования
    коллекций
    """

    if not key:
        def key(x):
            return x

    elements = OrderedDict()
    for iterable in iterables:
        iter_sort = iter(sorted(iterable, key=key))
        try:
            elements[iter_sort] = next(iter_sort)
        except StopIteration:
            pass

    while elements:
        result = min(elements.items(), key=lambda x: key(x[1]))
        yield result[1]

        try:
            elements[result[0]] = next(result[0])
        except StopIteration:
            del elements[result[0]]


def log_key(s):
    """Функция по строке лога возвращает ключ для её сравнения по времени"""
    time = re.search(r'\[(.+?) ', s)
    if time is not None:
        return datetime.datetime.strptime(time.group(1), '%d/%b/%Y:%H:%M:%S')
    return Exception


class TestTest(unittest.TestCase):
    def test_log_key1(self):
        test_string = '--[13/Nov/2022:21:22:43 +0600]'
        self.assertEqual(datetime.datetime(2022, 11, 13, 21, 22, 43),
                         log_key(test_string))

    def test_log_key3(self):
        test_string = '--[errordatetime]'
        self.assertEqual(Exception, log_key(test_string))

    def test_iter_merge1(self):
        arr1 = [4, 1, 7]
        arr2 = [9, 5, 7]
        result = [1, 4, 5, 7, 7, 9]
        i = 0
        for elem in merge(arr1, arr2):
            self.assertEqual(result[i], elem)
            i += 1

    def test_iter_merge2(self):
        arr1 = ['d', 'a', 'e']
        arr2 = ['b', 'd', 'c']
        result = ['a', 'b', 'c', 'd', 'd', 'e']
        i = 0
        for elem in merge(arr1, arr2):
            self.assertEqual(result[i], elem)
            i += 1
