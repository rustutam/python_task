#!/usr/bin/env python3

import argparse
import itertools
import os.path
import sys
from datetime import datetime
import struct


class TarParser:
    _HEADER_FMT1 = '100s8s8s8s12s12s8sc100s255s'
    _HEADER_FMT2 = '6s2s32s32s8s8s155s12s'
    _HEADER_FMT3 = '6s2s32s32s8s8s12s12s112s31x'
    _READ_BLOCK = 16 * 2 ** 20

    _FILE_TYPES = {
        b'0': 'Regular file',
        b'1': 'Hard link',
        b'2': 'Symbolic link',
        b'3': 'Character device node',
        b'4': 'Block device node',
        b'5': 'Directory',
        b'6': 'FIFO node',
        b'7': 'Reserved',
        b'D': 'Directory entry',
        b'K': 'Long linkname',
        b'L': 'Long pathname',
        b'M': 'Continue of last file',
        b'N': 'Rename/symlink command',
        b'S': "`sparse' regular file",
        b'V': "`name' is tape/volume header name"
    }

    @staticmethod
    def _parse_header(hdr):
        header1 = struct.unpack(TarParser._HEADER_FMT1, hdr)

        header2 = (header1[-1],)
        if header1[9].startswith(b'ustar\x00'):
            header2 = struct.unpack(TarParser._HEADER_FMT2, header1[-1])
        elif header1[9].startswith(b'ustar '):
            header2 = struct.unpack(TarParser._HEADER_FMT3, header1[-1])

        header = header1[:-1] + header2

        name = header[0]
        if len(header) > 16 and header[15]:
            name = b'/'.join((header[15], name))
        name = name.strip(b'\x00').decode()

        file_size = int(b'0' + header[4].strip(b'\x00'), 8)
        return header, name, file_size

    def _preprocess(self):
        self._files = {}
        self._fpts = []

        with open(self._filename, mode='rb') as f:
            hdr = f.read(512)
            while hdr:
                header, name, file_size = TarParser._parse_header(hdr)
                if header[7] == b'L':
                    name = f.read(512)[:file_size - 1].decode()
                    header, _, file_size = TarParser._parse_header(f.read(512))

                rest_bytes = (512 - file_size) % 512
                if name:
                    fdesc = (header, file_size, f.tell(), name)
                    self._files[name] = fdesc
                    self._fpts.append(fdesc)

                f.seek(file_size + rest_bytes, 1)

                hdr = f.read(512)

    def __init__(self, filename):
        '''
        Открывает arch-архив `filename' и производит его предобработку
        (если требуется)
        '''

        self._filename = filename
        self._preprocess()

    def extract(self, dest=os.getcwd()):
        '''
        Распаковывает данный arch-архив в каталог `dest'
        '''

        with open(self._filename, mode='rb') as arch:
            for file in self._fpts:
                arch.seek(file[2])
                if file[3][-1] == '/':
                    os.makedirs(dest + file[3])
                else:
                    with open(f'{dest}/{file[3]}', mode='wb') as f:
                        f.write(arch.read(file[1]))

    def files(self):
        '''
        Возвращает итератор имён файлов (с путями) в архиве
        '''

        def f(file):  # Ищет папку
            return file[-1] == '/'

        return itertools.filterfalse(f, self._files.keys())

    def parameter(self, name_option, f=lambda x: x.decode()):
        def wrapper(value):
            return name_option, f(value)

        return wrapper

    def mod_time(self, sec):
        sec = int(sec.decode())
        date = datetime.fromtimestamp(sec)
        return date.strftime('%m %b %Y %X')

    def file_stat(self, filename):
        '''
        Возвращает информацию о файле `filename' в архиве.

        Пример (некоторые поля могут отсутствовать, подробности см. в описании
        формата arch):
        [
            ('Filename', '/NSimulator'),
            ('Type', 'Directory'),
            ('Mode', '0000755'),
            ('UID', '1000'),
            ('GID', '1000'),
            ('Size', '0'),
            ('Modification time', '29 Mar 2014 03:52:45'),
            ('Checksum', '5492'),
            ('User name', 'victor'),
            ('Group name', 'victor')
        ]

        '''

        if filename not in self._files:
            raise ValueError(filename)
        info = [('Filename', filename)]
        file = self._files.get(filename)
        ind_parameter = {
            1: self.parameter('Mode'),
            2: self.parameter('UID'),
            3: self.parameter('GID'),
            4: self.parameter('Size', lambda x: int(x.decode())),
            5: self.parameter('Modification time', self.mod_time),
            6: self.parameter('Checksum'),
            7: self.parameter('Type', lambda x: self._FILE_TYPES.get(x)),
            8: self.parameter('Link'),
            9: self.parameter('Magic'),
            10: self.parameter('Version'),
            11: self.parameter('User name'),
            12: self.parameter('Group name'),
            13: self.parameter('Device major'),
            14: self.parameter('Device minor'),
            15: self.parameter('Prefix'),
            16: self.parameter('Last access time'),
            17: self.parameter('Last change time')
        }
        parameters = file[0]
        for i in range(1, len(parameters)):
            value = parameters[i].strip(b' ').strip(b'\x00')
            if len(value):
                info.append(ind_parameter[i](value))
        return info


def print_file_info(stat, f=sys.stdout):
    max_width = max(map(lambda s: len(s[0]), stat))
    for field in stat:
        print("{{:>{}}} : {{}}".format(max_width).format(*field), file=f)


def main():
    parser = argparse.ArgumentParser(
        usage='{} [OPTIONS] FILE'.format(os.path.basename(sys.argv[0])),
        description='arch extractor')
    parser.add_argument('-l', '--list', action='store_true', dest='ls',
                        help='list the contents of an archive')
    parser.add_argument('-x', '--extract', action='store_true', dest='extract',
                        help='extract files from an archive')
    parser.add_argument('-i', '--info', action='store_true', dest='info',
                        help='get information about files in an archive')
    parser.add_argument('fn', metavar='FILE',
                        help='name of an archive')

    args = parser.parse_args()

    if not (args.ls or args.extract or args.info):
        sys.exit("Error: action must be specified")

    try:
        arch = TarParser(args.fn)

        if args.info:
            for fn in sorted(arch.files()):
                print_file_info(arch.file_stat(fn))
                print()
        elif args.ls:
            for fn in sorted(arch.files()):
                print(fn)

        if args.extract:
            arch.extract()
    except Exception as e:
        sys.exit(e)


if __name__ == '__main__':
    main()
