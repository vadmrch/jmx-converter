import re
from argparse import ArgumentParser
import json
import configparser
from datetime import datetime

config = configparser.ConfigParser()
config.read('filters.conf')
CT_HEADER_FILTER = config.get('Filter rules', 'content-type_filter')
CT_URL_FILTER = config.get('Filter rules', 'url-based_filter')


def read_har(path):
    with open(path) as raw_har:
        har_dict = json.load(raw_har)
    return har_dict


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


def request_parser(request):
    request_protocol = re.search('^https|^http', request['url']).group(0)
    request_method = request['method']
    request_host = request['url'].split('/')[2]
    try:
        request_path = '/' + '/'.join(request['url'].split('/')[3:]).split('?')[0]
        request_params = request['url'].split('?')[1].split('&')
    except IndexError:
        request_path = '/' + '/'.join(request['url'].split('/')[3:])
        request_params = []
    try:
        request_body = request['postData']['text']
    except KeyError:
        request_body = None
    return request_protocol, request_method, request_host, request_path, request_params, request_body


def main(args):
    har = read_har(args.har_file)
    har_name = args.har_file.replace('\\', '/').split('/')[-1].split('.')[0]
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    jmx_name = f'{har_name}_{timestamp}.jmx'
    for entry in har['log']['entries']:
        if not args.no_filter:
            if ct_url_check(entry):
                continue
            if ct_header_check(entry):
                continue
        print(request_parser(entry['request']))
    print(jmx_name)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('har_file',
                        help='Path to .har file')
    parser.add_argument('-nf', '--no-filter', action='store_true',
                        help='Disables filtering out static requests. Filter settings - filters.conf')
    # TODO Add host filter
    # parser.add_argument('-hf', '--host-filter', action='store_true',
    #                     help='Enable host filter')
    # TODO Add header manager option
    # parser.add_argument('-nh', '--no-headers', action='store_false',
    #                     help='Don\'t add Header Manager for samplers')
    # TODO Add custom path and name for .jmx
    # parser.add_argument('-jp', '--jmx-path',
    #                     help='Custom path to save .jmx')
    # parser.add_argument('-jn', '--jmx-name',
    #                     help='Custom name for .jmx file. Default is same as .har\'s name + timestamp')
    cl_args = parser.parse_args()
    main(cl_args)
