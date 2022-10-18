from urllib.request import urlopen
from collections import Counter

import re


def stat_names_find(html_page):
    pos = 0
    names = []
    while True:
        start = html_page.find('/>', pos)
        if start == -1:
            break
        end = html_page.find('</a', start)
        _, name = html_page[start + 2: end].split()
        names.append(name)
        pos = end
    print(names)
    from collections import Counter

    names_stat = Counter(names)
    print(names_stat.most_common())


def stat_names_re(html_page):
    reg = r'/>[а-яА-ЯёЁ]+ ([а-яА-ЯёЁ]+)'
    names = re.findall(reg, html_page)
    names_stat = Counter(names)
    return names_stat.most_common()


if __name__ == '__main__':
    URL = "http://shannon.usu.edu.ru/ftp/python/hw2/home.html"
    with urlopen(URL) as response:
        html_page = response.read().decode('cp1251')
    print(stat_names_re(html_page))