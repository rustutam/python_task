from urllib.request import urlopen
from urllib.parse import quote
from urllib.parse import unquote
from urllib.error import URLError, HTTPError
from collections import deque
import re


def get_content(name):
    """
    Функция возвращает содержимое вики-страницы name из русской Википедии.
    В случае ошибки загрузки или отсутствия страницы возвращается None.
    """

    try:
        with urlopen('https://ru.wikipedia.org/wiki/' + quote(name)) as page:
            return page.read().decode('utf-Homework_8', errors='ignore')
    except (URLError, HTTPError):
        return None


def extract_content(page):
    """
    Функция принимает на вход содержимое страницы и возвращает 2-элементный
    tuple, первый элемент которого — номер позиции, с которой начинается
    содержимое статьи, второй элемент — номер позиции, на котором заканчивается
    содержимое статьи.
    Если содержимое отсутствует, возвращается (0, 0).
    """
    begin_index = page.find('<div id="mw-content-text"')
    end_index = page.find('<div id="catlinks"')
    if begin_index == -1 or end_index == -1:
        return 0, 0
    return begin_index, end_index


def extract_links(page, begin, end):
    """
    Функция принимает на вход содержимое страницы и начало и конец интервала,
    задающего позицию содержимого статьи на странице и возвращает все имеющиеся
    ссылки на другие вики-страницы без повторений и с учётом регистра.
    """
    if page:
        reg = r'(?:\'|")/wiki/([\w\-_.,;%]+)(?:\'|")(?: class="mw-redirect")?'
        links = re.findall(reg, page[begin:end])
        s = []
        for link in links:
            s.append(unquote(link))
        return set(s)
    else:
        return None


def find_chain(start, finish):
    """
    Функция принимает на вход название начальной и конечной статьи и возвращает
    список переходов, позволяющий добраться из начальной статьи в конечную.
    Первым элементом результата должен быть start, последним — finish.
    Если построить переходы невозможно, возвращается None.
    """
    if start == finish:
        return [start, finish]
    visited = set()
    to_visit = deque()
    path = dict()
    to_visit.appendleft(start)
    while len(to_visit) != 0:
        actual = to_visit.pop()
        visited.add(actual)
        page = get_content(actual)
        if not page:
            return None
        pos = extract_content(page)
        begin_index = pos[0]
        end_index = pos[1]
        links_in_page = extract_links(page, begin_index, end_index)
        for link in links_in_page:
            if link not in visited:
                to_visit.appendleft(link)
                path[link] = actual
            if link == finish:
                answer = [finish]
                actual = finish
                while actual != start:
                    actual = path[actual]
                    answer.append(actual)
                return list(reversed(answer))
    return None


def main():
    pass


if __name__ == '__main__':
    main()
