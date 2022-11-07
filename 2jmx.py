from argparse import ArgumentParser
import json
import configparser
from datetime import datetime
from har_parser import har_request_parser
from jmx_builder import *

config = configparser.ConfigParser()
config.read('filters.conf')
CT_HEADER_FILTER = config.get('Filter rules', 'content-type_filter')
CT_URL_FILTER = config.get('Filter rules', 'url-based_filter')
HOST_FILTER = config.get('Filter rules', 'host_filter')


def read_source(path):
    with open(path) as raw_har:
        source_dict = json.load(raw_har)
    return source_dict


def make_jmx_name(path, param):
    if path is not None:
        har_name = path.replace('\\', '/').split('/')[-1].split('.')[0]
        timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        jmx_name = f'{har_name}_{timestamp}.jmx'
    else:
        jmx_name = param
        if len(jmx_name.split('.')) > 1:
            jmx_name = jmx_name.split('.')[0] + '.jmx'
        else:
            jmx_name = jmx_name + '.jmx'
    return jmx_name


# Check content type basen on Content-type header
def ct_header_check(entry):
    for response_header in entry['response']['headers']:
        if response_header['name'].lower() == 'content-type':
            # .split(';') in case encoding is in header ("text/css; charset=UTF-8")
            if response_header['value'].split(';')[0] in CT_HEADER_FILTER:
                return True
            else:
                return False


# Check content type basen on url
def ct_url_check(entry):
    # Check the last part of url ("http://host.com/image.PNG")
    # .split('?') in case there are params in url
    if entry['request']['url'].split('.')[-1].split('?')[0] in CT_URL_FILTER:
        return True
    else:
        return False


# TODO Add wildcards support
def host_filter(host):
    if host in HOST_FILTER:
        return True
    else:
        return False


def main(args):
    file = read_source(args.source_file)
    if args.jmx_name:
        jmx_name = make_jmx_name(None, args.jmx_name)
    else:
        jmx_name = make_jmx_name(args.source_file, None)
    for entry in file['log']['entries']:
        request = har_request_parser(entry['request'])
        if not args.no_filter:
            if ct_url_check(entry):
                continue
            if ct_header_check(entry):
                continue
        if args.host_filter:
            if host_filter(request['host']):
                continue


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('source_file',
                        help='Path to source_file file. Supported types: .har')
    parser.add_argument('-nf', '--no-filter', action='store_true',
                        help='Disables filtering out static requests. Filter settings - filters.conf')
    parser.add_argument('-hf', '--host-filter', action='store_true',
                        help='Enable host filter')
    # TODO Add header manager option
    # parser.add_argument('-nh', '--no-headers', action='store_false',
    #                     help='Don\'t add Header Manager for samplers')
    # TODO Add custom path and name for .jmx
    # parser.add_argument('-jp', '--jmx-path',
    #                     help='Custom path to save .jmx')
    parser.add_argument('-jn', '--jmx-name',
                        help='Custom name for .jmx file. Default is same as .har\'s name + timestamp')
    cl_args = parser.parse_args()
    main(cl_args)
