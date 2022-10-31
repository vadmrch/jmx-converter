from argparse import ArgumentParser
import json
import configparser

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


def write_jmx(filter_option):
    har = read_har(args.har_file)
    for entry in har['log']['entries']:
        if not filter_option:
            if ct_url_check(entry):
                continue
            if ct_header_check(entry):
                continue
        print(entry['request']['url'])


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('har_file', help='Path to .har file')
    parser.add_argument('-nf', '--no-filter', action='store_true', help='Disables filtering out static requests. Filter settings - filters.conf')
    args = parser.parse_args()
    write_jmx(args.no_filter)
