import re
import datetime
import unittest


class Parsing:
    ip = ""
    date_and_time = ""
    page = ""
    browser = ""
    time_of_work = -1
    reg = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' \
          r' - - \[(\S+?):\d+?:\d+?:\d+? .+?\] ' \
          r'"[A-Z]{3,7} (\S+).+?" \d+ \d+ ".+?" "(.+?)"(?: (\d*))?'

    def parsing(self, line):
        if obj := re.search(self.reg, line):
            self.ip = obj.group(1)
            self.date_and_time = obj.group(2)
            self.page = obj.group(3)
            self.browser = obj.group(4)
            if obj.group(5):
                self.time_of_work = int(obj.group(5))
            else:
                self.time_of_work = None
            return True


class Statistics:
    stat_slow_page = ["page", -1]
    stat_fast_page = ["page", 10 ** 15]
    stat_slow_page_av = []
    stat_popular_page = []
    stat_active_client = []
    stat_popular_browser = []
    stat_client_by_day = {}

    time_num_stat = {}
    client_stat = {}
    browser_stat = {}
    time_client_stat = {}

    def add_line(self, line):
        string = Parsing()
        if string.parsing(line):
            self.slow_page(string.page, string.time_of_work)
            self.fast_page(string.page, string.time_of_work)
            self.add_page_num_time_stat(string.page,
                                        string.time_of_work)
            self.add_stat_active_client(string.ip)
            self.add_browser_stat(string.browser)
            self.add_time_client_stat(string.ip, string.date_and_time)

    def slow_page(self, page, time):
        if time is None:
            return
        if self.stat_slow_page[1] <= int(time):
            if self.stat_slow_page[0] != page:
                self.stat_slow_page[0] = page
            self.stat_slow_page[1] = int(time)

    def fast_page(self, page, time):
        if time is None:
            return
        if self.stat_fast_page[1] >= int(time):
            if self.stat_fast_page[0] != page:
                self.stat_fast_page[0] = page
            self.stat_fast_page[1] = int(time)

    def add_page_num_time_stat(self, page, time):
        if time is None:
            return
        if page in self.time_num_stat:
            self.time_num_stat[page][0] += 1
            self.time_num_stat[page][1] += time
        else:
            self.time_num_stat[page] = [1, time]

    def slow_page_av(self):
        for i in self.time_num_stat:
            self.time_num_stat[i][1] = self.time_num_stat[i][1] / \
                                       self.time_num_stat[i][0]
        stat = {}
        for i in self.time_num_stat:
            stat[i] = self.time_num_stat[i][1]
        self.stat_slow_page_av = max(stat, key=stat.get)

    def popular_page(self):
        stat = {}
        for i in self.time_num_stat:
            stat[i] = self.time_num_stat[i][0]
        sorted(stat.items())
        self.stat_popular_page = max(stat, key=stat.get)

    def add_stat_active_client(self, client):
        if client not in self.client_stat:
            self.client_stat[client] = 1
        else:
            self.client_stat[client] += 1

    def active_client(self):
        sorted(self.client_stat.items())
        self.stat_active_client = max(self.client_stat,
                                      key=self.client_stat.get)

    def add_browser_stat(self, browser):
        if browser in self.browser_stat:
            self.browser_stat[browser] += 1
        else:
            self.browser_stat[browser] = 1

    def popular_browser(self):
        sorted(self.browser_stat.items())
        self.stat_popular_browser = max(self.browser_stat,
                                        key=self.browser_stat.get)

    def add_time_client_stat(self, client, time):
        day = datetime.datetime.strptime(time, '%d/%b/%Y').date()
        if day not in self.time_client_stat:
            self.time_client_stat[day] = {}
        if client in self.time_client_stat[day]:
            self.time_client_stat[day][client] += 1
        else:
            self.time_client_stat[day][client] = 1

    def active_client_by_day(self):
        sorted(self.time_client_stat.items())
        for i in self.time_client_stat:
            sorted(self.time_client_stat[i].items())
            self.stat_client_by_day[i] = max(self.time_client_stat[i],
                                             key=self.time_client_stat[i].get)

    def results(self):
        self.slow_page_av()
        self.popular_page()
        self.active_client()
        self.popular_browser()
        self.active_client_by_day()
        return {
            'FastestPage': self.stat_fast_page[0],
            'MostActiveClient': self.stat_active_client,
            'MostActiveClientByDay': self.stat_client_by_day,
            'MostPopularBrowser': self.stat_popular_browser,
            'MostPopularPage': self.stat_popular_page,
            'SlowestAveragePage': self.stat_slow_page_av,
            'SlowestPage': self.stat_slow_page[0]}


def make_stat():
    return Statistics()


class LogStatTests(unittest.TestCase):
    def setUp(self):
        self.parser = Statistics()
        self.parser.add_line(
            '192.100.10.10 - - [17/Feb/2013:06:37:21 +0600] "GET '
            '/tv/useUser HTTP/1.1" 200 432 "asd" "Yandex" 2')
        self.parser.add_line(
            '192.100.12.10 - - [17/Feb/2013:06:37:21 +0600] "GET '
            '/tv/Needed HTTP/1.1" 200 432 "asd" "Yandex" 2')
        self.parser.add_line(
            '192.168.12.10 - - [17/Feb/2013:06:37:21 +0600] "GET '
            '/tv/useUser HTTP/1.1" 200 432 "asd" "Yandex" 1')

    def test_average_time(self):
        self.parser.slow_page_av()
        self.assertEqual(self.parser.stat_slow_page_av,
                         "/tv/Needed")

    def test_most_active_client(self):
        self.parser.active_client()
        self.assertEqual(self.parser.stat_active_client,
                         '192.100.10.10')
