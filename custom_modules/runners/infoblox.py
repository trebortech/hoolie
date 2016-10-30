'''
Infoblox runner to manage IPAM

:depends:
    requests
    json

'''
from __future__ import absolute_import

import salt.utils.sdb as sdb

import logging

log = logging.getLogger(__name__)

try:
    import json
    import requests
    HAS_IMPORTS = True
except ImportError:
    HAS_IMPORTS = False


def __virtual__():
    if HAS_IMPORTS:
        return True
    return (False, 'The infoblox runner cannot start')


def _send_server(module, method='POST', opts=None, data=None):

    if opts is None:
        opts = __opts__
    config = opts['engines'][0]['infoblox']
    server = config['server']
    api_version = config['api_version']
    user = config['user']
    password = config['password']
    sslVerify = config['sslVerify']
    headers = {'content-type': 'application/json'}

    ib_url = 'https://{0}/wapi/{1}/{2}'.format(
        server,
        api_version,
        module)

    if method == 'POST':
        requestset = requests.post(ib_url,
                                   auth=(user, password),
                                   verify=sslVerify,
                                   data=json.dumps(data),
                                   headers=headers)
    elif method == 'DELETE':
        requestset = requests.delete(ib_url,
                                     auth=(user, password),
                                     verify=sslVerify,
                                     data=json.dumps(data),
                                     headers=headers)
    elif method == 'GET':
        requestset = requests.get(ib_url,
                                  auth=(user, password),
                                  verify=sslVerify,
                                  data=json.dumps(data),
                                  headers=headers)

    return requestset


def get_ip(hostname, domain, subnet, opts=None):

    if opts is None:
        opts = __opts__

    # Get Network view from SDB
    ib_ds = 'sdb://infoblox/{0}'.format(subnet)
    ib_module = sdb.sdb_get(ib_ds, opts)

    # Get IP Address
    ret = _send_server("{0}?_function=next_available_ip".format(ib_module), opts=opts)

    new_ip = {}
    if ret.status_code == 200:
        new_ip['ipv4addr'] = ret.json()['ips'][0]
    else:
        return False

    hostname_payload = {}
    hostname_payload['ipv4addrs'] = [new_ip]
    hostname_payload['name'] = '{0}.{1}'.format(hostname, domain)

    ret = _send_server("record:host", data=hostname_payload, opts=opts)

    if ret.ok:
        return new_ip
    else:
        return False


def set_host(hostname, domain, ipaddress, opts=None):

    if opts is None:
        opts = __opts__

    new_ip = {}
    new_ip['ipv4addr'] = ipaddress
    hostname_payload = {}
    hostname_payload['ipv4addrs'] = [new_ip]
    hostname_payload['name'] = '{0}.{1}'.format(hostname, domain)

    ret = _send_server("record:host", data=hostname_payload, opts=opts)

    if ret.ok:
        return True
    else:
        return False


def remove_host(hostname, domain):

    # Search for host

    host_payload = {}
    host_payload['name'] = '{0}.{1}'.format(hostname, domain)

    ret = _send_server("record:host", method='GET', data=host_payload)

    if ret.ok:
        hostid = ret.json()[0]['_ref']
    else:
        return False

    # Delete host if found
    ret = _send_server(hostid, method='DELETE')

    if ret.ok:
        return True
    else:
        return False
