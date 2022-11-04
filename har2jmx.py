import re
from argparse import ArgumentParser
import json
import configparser
from datetime import datetime

config = configparser.ConfigParser()
config.read('filters.conf')
CT_HEADER_FILTER = config.get('Filter rules', 'content-type_filter')
CT_URL_FILTER = config.get('Filter rules', 'url-based_filter')
HOST_FILTER = config.get('Filter rules', 'host_filter')


def read_har(path):
    with open(path) as raw_har:
        har_dict = json.load(raw_har)
    return har_dict


def make_jmx_name(path):
    har_name = path.replace('\\', '/').split('/')[-1].split('.')[0]
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    jmx_name = f'{har_name}_{timestamp}.jmx'
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


def params_parser(params):
    params_list = []
    for param in params:
        split_param = param.split('=')
        # For nameless parameters
        if len(split_param) > 1:
            param_name = split_param[0]
            param_value = split_param[1]
        else:
            param_name = None
            param_value = split_param[0]

        param_dict = {'name': param_name,
                      'value': param_value}
        params_list.append(param_dict)
    return params_list


def url_parser(request):
    try:
        request_protocol = re.search('^(.+?)://', request['url']).group(1)
    except AttributeError:
        request_protocol = None

    split_url = request['url'].split('/')
    # Adjust index at url parsing in case there is no protocol
    if request_protocol:
        i = 2
    else:
        i = 0
    request_host = split_url[i]

    # In case there is Port in url
    if ':' in request_host:
        request_port = request_host.split(':')[1]
        request_host = request_host.split(':')[0]
    else:
        request_port = None

    try:
        request_path = '/' + '/'.join(split_url[i+1:]).split('?')[0]
        request_params = request['url'].split('?')[1].split('&')
    except IndexError:
        request_path = '/' + '/'.join(split_url[i+1:])
        request_params = None
    # Convert list ['name=value'...] to list of dictionaries [{'name':name, 'value':value}...] for more comfort later
    if request_params:
        request_params = params_parser(request_params)

    if request['bodySize'] > 0:
        try:
            request_body = request['postData']['text']
        except KeyError:
            request_body = 'Failed to parse body data, but it has to be here'
    else:
        request_body = None

    parsed_url = {
        'method': request['method'],
        'protocol': request_protocol,
        'host': request_host,
        'port': request_port,
        'path': request_path,
        'params': request_params,
        'body': request_body
    }
    return parsed_url


# TODO Add wildcards support
def host_filter(host):
    if host in HOST_FILTER:
        return True
    else:
        return False


def main(args):
    har = read_har(args.har_file)
    jmx_name = make_jmx_name(args.har_file)
    for entry in har['log']['entries']:
        if not args.no_filter:
            if ct_url_check(entry):
                continue
            if ct_header_check(entry):
                continue
        if args.host_filter:
            if host_filter(url_parser(entry['request'])['host']):
                continue
        print(url_parser(entry['request']))
    print(jmx_name)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('har_file',
                        help='Path to .har file')
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
    # parser.add_argument('-jn', '--jmx-name',
    #                     help='Custom name for .jmx file. Default is same as .har\'s name + timestamp')
    cl_args = parser.parse_args()
    main(cl_args)
