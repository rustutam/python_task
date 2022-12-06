import os
import sys
import itertools


def project_stats(path, extensions):
    """
    Вернуть число строк в исходниках проекта.
    
    Файлами, входящими в проект, считаются все файлы
    в папке ``path`` (и подпапках), имеющие расширение
    из множества ``extensions``.
    """

    return sum(map(number_of_lines, with_extensions(extensions,
                                                    iter_filenames(path))))


def total_number_of_lines(filenames):
    """
    Вернуть общее число строк в файлах ``filenames``.
    """

    return sum(map(number_of_lines, filenames))


def number_of_lines(filename):
    """ 
    Вернуть число строк в файле.
    """
    if os.stat(filename).st_size == 0:
        return 0
    with open(filename, 'rb') as file:
        def f(x):
            if b'\n' in x:
                return 1
            else:
                return 0

        return sum(map(f, file), start=1)


def iter_filenames(path):
    """
    Итератор по именам файлов в дереве.
    """

    def make_path(argumets):
        return map(lambda filename: argumets[0] + '\\' + filename, argumets[2])

    directory_tree = os.walk(path)
    return itertools.chain(*map(make_path, directory_tree))


def with_extensions(extensions, filenames):
    """
    Оставить из итератора ``filenames`` только
    имена файлов, у которых расширение - одно из ``extensions``.    
    """

    return itertools.filterfalse(lambda x: get_extension(x) not in extensions,
                                 filenames)


def get_extension(filename):
    """ Вернуть расширение файла """

    _, extension = os.path.splitext(filename)
    return extension


def print_usage():
    print("Usage: python project_sourse_stats.py <project_path>")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print_usage()
        sys.exit(1)
    project_path = sys.argv[1]
    print(project_stats(project_path, {'.cs'}))
