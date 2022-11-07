import xml.etree.ElementTree as ET


def get_root():
    root = ET.Element('jmeterTestPlan', attrib={'version': '1.2', 'properties': '5.0', 'jmeter': '5.5'})
    return root


def add_hash_tree(elem):
    hash_tree = ET.SubElement(elem, 'hashTree')
    return hash_tree


def make_test_plan(elem):
    tplan = ET.SubElement(elem, 'TestPlan', attrib={'guiclass': 'TestPlanGui',
                                                    'testclass': 'TestPlan',
                                                    'testname': 'Test Plan',
                                                    'enabled': 'true'})
    ET.SubElement(tplan, 'stringProp', attrib={'name': 'TestPlan.comments'}).text = None
    ET.SubElement(tplan, 'boolProp', attrib={'name': 'TestPlan.functional_mode'}).text = 'false'
    ET.SubElement(tplan, 'boolProp', attrib={'name': 'TestPlan.tearDown_on_shutdown'}).text = 'true'
    ET.SubElement(tplan, 'boolProp', attrib={'name': 'TestPlan.serialize_threadgroups'}).text = 'false'
    element_prop = ET.SubElement(tplan, 'elementProp', attrib={'name': 'TestPlan.user_defined_variables',
                                                               'elementType': 'Arguments',
                                                               'guiclass': 'ArgumentsPanel',
                                                               'testclass': 'Arguments',
                                                               'testname': 'User Defined Variables',
                                                               'enabled': 'true'})
    ET.SubElement(element_prop, 'collectionProp', attrib={'name': 'Arguments.arguments'})
    ET.SubElement(tplan, 'stringProp', attrib={'name': 'TestPlan.user_define_classpath'}).text = None


def add_tg(elem):
    tgroup = ET.SubElement(elem, 'ThreadGroup', attrib={'guiclass': 'ThreadGroupGui',
                                                        'testclass': 'ThreadGroup',
                                                        'testname': 'Thread Group',
                                                        'enabled': 'true'})
    ET.SubElement(tgroup, 'stringProp', attrib={'name': 'ThreadGroup.on_sample_error'}).text = 'continue'
    elem_prop = ET.SubElement(tgroup, 'elementProp', attrib={'name': 'ThreadGroup.main_controller',
                                                             'elementType': 'LoopController',
                                                             'guiclass': 'LoopControlPanel',
                                                             'testclass': 'LoopController',
                                                             'testname': 'LoopController',
                                                             'enabled': 'true'})
    ET.SubElement(elem_prop, 'boolProp', attrib={'name': 'LoopController.continue_forever'}).text = 'false'
    ET.SubElement(elem_prop, 'stringProp', attrib={'name': 'LoopController.loops'}).text = '1'
    ET.SubElement(tgroup, 'stringProp', attrib={'name': 'ThreadGroup.num_threads'}).text = '1'
    ET.SubElement(tgroup, 'stringProp', attrib={'name': 'ThreadGroup.ramp_time'}).text = '1'
    ET.SubElement(tgroup, 'boolProp', attrib={'name': 'ThreadGroup.scheduler'}).text = 'false'
    ET.SubElement(tgroup, 'stringProp', attrib={'name': 'ThreadGroup.duration'}).text = ''
    ET.SubElement(tgroup, 'stringProp', attrib={'name': 'ThreadGroup.delay'}).text = ''
    ET.SubElement(tgroup, 'boolProp', attrib={'name': 'ThreadGroup.same_user_on_next_iteration'}).text = 'true'


def add_sampler(elem, req):
    sampler = ET.SubElement(elem, 'HTTPSamplerProxy', attrib={'guiclass': 'HttpTestSampleGui',
                                                              'testclass': 'HTTPSamplerProxy',
                                                              'testname': 'Sampler Name',
                                                              'enabled': 'true'})
    # Add parameters
    if req['params']:
        elem_p_s = ET.SubElement(sampler, 'elementProp', attrib={'name': 'HTTPsampler.Arguments',
                                                                 'elementType': 'Arguments',
                                                                 'guiclass': 'HTTPArgumentsPanel',
                                                                 'testclass': 'Arguments',
                                                                 'testname': 'User Defined Variables',
                                                                 'enabled': 'true'})
        collec_p_a = ET.SubElement(elem_p_s, 'collectionProp', attrib={'name': 'Arguments.arguments'})
        for param in req['params']:
            elem_p_a = ET.SubElement(collec_p_a, 'elementProp', attrib={'name': param['name'],
                                                                        'elementType': 'HTTPArgument'})
            ET.SubElement(elem_p_a, 'boolProp', attrib={'name': 'HTTPArgument.always_encode'}).text = 'false'
            ET.SubElement(elem_p_a, 'stringProp', attrib={'name': 'Argument.value'}).text = param['value']
            ET.SubElement(elem_p_a, 'stringProp', attrib={'name': 'Argument.metadata'}).text = '='
            ET.SubElement(elem_p_a, 'boolProp', attrib={'name': 'HTTPArgument.use_equals'}).text = 'true'
            ET.SubElement(elem_p_a, 'stringProp', attrib={'name': 'Argument.name'}).text = param['name']

    # Add body data
    if req['body']:
        ET.SubElement(sampler, 'boolProp', attrib={'name': 'HTTPSampler.postBodyRaw'}).text = 'true'
        elem_p_b = ET.SubElement(sampler, 'elementProp', attrib={'name': 'HTTPsampler.Arguments',
                                                                 'elementType': 'Arguments'})
        collec_p_b = ET.SubElement(elem_p_b, 'collectionProp', attrib={'name': 'Arguments.arguments'})
        epb = ET.SubElement(collec_p_b, 'elementProp', attrib={'name': '', 'elementType': 'HTTPArgument'})
        ET.SubElement(epb, 'boolProp', attrib={'name': 'HTTPArgument.always_encode'}).text = 'false'
        ET.SubElement(epb, 'stringProp', attrib={'name': 'Argument.value'}).text = req['body']
        ET.SubElement(epb, 'stringProp', attrib={'name': 'Argument.metadata'}).text = '='
    # Add base elements
    ET.SubElement(sampler, 'stringProp', attrib={'name': 'HTTPSampler.domain'}).text = req['host']
    ET.SubElement(sampler, 'stringProp', attrib={'name': 'HTTPSampler.port'}).text = req['port']
    ET.SubElement(sampler, 'stringProp', attrib={'name': 'HTTPSampler.protocol'}).text = req['protocol']
    ET.SubElement(sampler, 'stringProp', attrib={'name': 'HTTPSampler.contentEncoding'}).text = None
    ET.SubElement(sampler, 'stringProp', attrib={'name': 'HTTPSampler.path'}).text = req['path']
    ET.SubElement(sampler, 'stringProp', attrib={'name': 'HTTPSampler.method'}).text = req['method']
    ET.SubElement(sampler, 'boolProp', attrib={'name': 'HTTPSampler.follow_redirects'}).text = 'true'
    ET.SubElement(sampler, 'boolProp', attrib={'name': 'HTTPSampler.auto_redirects'}).text = 'false'
    ET.SubElement(sampler, 'boolProp', attrib={'name': 'HTTPSampler.use_keepalive'}).text = 'true'
    ET.SubElement(sampler, 'boolProp', attrib={'name': 'HTTPSampler.DO_MULTIPART_POST'}).text = 'false'
    ET.SubElement(sampler, 'stringProp', attrib={'name': 'HTTPSampler.embedded_url_re'}).text = None
    ET.SubElement(sampler, 'stringProp', attrib={'name': 'HTTPSampler.connect_timeout'}).text = None
    ET.SubElement(sampler, 'stringProp', attrib={'name': 'HTTPSampler.response_timeout'}).text = None


def beautify_jmx(elem, level=0, tab='  ', nline='\n'):
    i = nline + level * tab
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + tab
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            beautify_jmx(elem, level + 1, tab, nline)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def save_jmx(root):
    # TODO REMOVE AFTER DEBUG
    ET.dump(root)
    tree = ET.ElementTree(root)
    tree.write('test.jmx', encoding='UTF-8', xml_declaration=True)
