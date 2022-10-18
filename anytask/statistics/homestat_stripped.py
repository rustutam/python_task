def make_stat(filename):
    with open(filename, encoding='cp1251') as response:
        html_page = response.read()
    year_pos = 0
    stat = {}
    exceptions = ['Илья', 'Лёва', 'Никита', 'Игорь']
    while True:
        year_start = html_page.find('<h3>', year_pos)
        if year_start == -1:
            break
        year_end = html_page.find('</h3>', year_start)
        year = html_page[year_start + 4: year_end]
        name_pos = year_end
        male_names = []
        female_names = []
        year_pos = year_end
        next_year_start = html_page.find('<h3>', year_end)
        if next_year_start == -1:
            next_year_start = 10000000
        while True:
            start = html_page.find('/">', name_pos)
            if start > next_year_start or start == -1:
                break
            end = html_page.find('</a', start)
            name = html_page[start + 2: end].split()[1]
            if name[len(name) - 1] == 'а' or name[len(name) - 1] == 'я' \
                    or name[len(name) - 1] == 'ь':
                if name in exceptions:
                    male_names.append(name)
                else:
                    female_names.append(name)
            else:
                male_names.append(name)
            name_pos = end
        stat[year] = {'male': male_names, 'female': female_names}
    return stat


def extract_years(stat):
    years_list = list(stat.keys())
    years_list.sort()
    return years_list


def extract_general(stat):
    from collections import Counter
    names = []
    for i in stat.keys():
        for j in stat[i]:
            names_array = stat[i][j]
            for name in names_array:
                names.append(name)
    names = Counter(names)
    return names.most_common()


def extract_general_male(stat):
    from collections import Counter
    names = []
    for i in stat.keys():
        names_array = stat[i]['male']
        for name in names_array:
            names.append(name)
    names = Counter(names)
    return names.most_common()


def extract_general_female(stat):
    from collections import Counter
    names = []
    for i in stat.keys():
        names_array = stat[i]['female']
        for name in names_array:
            names.append(name)
    names = Counter(names)
    return names.most_common()


def extract_year(stat, year):
    from collections import Counter
    names = []
    for j in stat[year]:
        names_array = stat[year][j]
        for name in names_array:
            names.append(name)
    names = Counter(names)
    return names.most_common()


def extract_year_male(stat, year):
    from collections import Counter
    names = []
    names_array = stat[year]['male']
    for name in names_array:
        names.append(name)
    names = Counter(names)
    return names.most_common()


def extract_year_female(stat, year):
    from collections import Counter
    names = []
    names_array = stat[year]['female']
    for name in names_array:
        names.append(name)
    names = Counter(names)
    return names.most_common()


if __name__ == '__main__':
    pass
