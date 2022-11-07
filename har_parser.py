import re


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


def har_request_parser(request):
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
        request_port = str(request_host.split(':')[1])
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

    parsed_request = {
        'method': request['method'],
        'protocol': request_protocol,
        'host': request_host,
        'port': request_port,
        'path': request_path,
        'params': request_params,
        'body': request_body
    }
    return parsed_request
