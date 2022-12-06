import operator
import re
import argparse


def read_file(filename):
    statistics = {}
    ip_stat = {}
    resource_stat = {}
    regex_for_ip = re.compile(r'(.+?),')
    regex_for_link = re.compile(r' (/.+?),')
    with open(filename, errors='ignore') as logs:
        for line in logs:
            ip = re.search(regex_for_ip, line)
            link = re.search(regex_for_link, line)
            if ip:
                ip_key = ip.group(1)
                if ip_key in ip_stat:
                    ip_stat[ip_key] += 1
                else:
                    ip_stat[ip_key] = 1
            if link:
                resource_key = link.group(1)
                if resource_key in resource_stat:
                    resource_stat[resource_key] += 1
                else:
                    resource_stat[resource_key] = 1
    statistics['ip'] = ip_stat
    statistics['resource'] = resource_stat
    return statistics


def get_popular(dict_stat):
    return max(dict_stat.items(), key=operator.itemgetter(1))[0]


def popular_client(stat):
    return get_popular(stat['ip'])


def popular_resource(stat):
    return get_popular(stat['resource'])


def arg_parser():
    usage = 'Simple run: python %(prog)s log_name [key]'
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('file_name', type=str, help='Input file name')
    group = parser.add_argument_group('keys')
    group.add_argument('-r', '--resource',
                       action='store_true',
                       help='get the most popular resource  from log')
    group.add_argument('-c', '--client',
                       action='store_true',
                       help='get the most popular client  from log')
    return parser


if __name__ == '__main__':
    arg_parser = arg_parser()
    args = arg_parser.parse_args()
    if not (args.client or args.resource):
        print(f'error: need a key')
    elif stat := read_file(args.file_name):
        if args.client:
            print(popular_client(stat))
        if args.resource:
            print(popular_resource(stat))
