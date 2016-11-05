'''
xMatter runner


:config example:
engines:
  xmatters:
    server: demo.na2.xmatters.com
    api: api/integration/1/functions/
    uuid: 2e....2c-d..b-4..50-9...b-793.....af
    user:
    password:
    sslVerify: False


:depends:
    requests
    json


'''
from __future__ import absolute_import
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
    return (False, 'The xMatters runner cannot start')


def _send_server(method='POST', opts=None, data=None):

    if opts is None:
        opts = __opts__
    config = opts['engines']['xmatters']
    server = config['server']
    api = config['api']
    uuid = config['uuid']
    user = config['user']
    password = config['password']
    sslVerify = config['sslVerify']
    headers = {'content-type': 'application/json'}

    xm_url = 'https://{0}/{1}/{2}/triggers'.format(
        server,
        api,
        uuid)

    if method == 'POST':
        requestset = requests.post(xm_url,
                                   auth=(user, password),
                                   verify=sslVerify,
                                   data=json.dumps(data),
                                   headers=headers)
    elif method == 'DELETE':
        requestset = requests.delete(xm_url,
                                     auth=(user, password),
                                     verify=sslVerify,
                                     data=json.dumps(data),
                                     headers=headers)
    elif method == 'GET':
        requestset = requests.get(xm_url,
                                  auth=(user, password),
                                  verify=sslVerify,
                                  data=json.dumps(data),
                                  headers=headers)

    return requestset


def create_event(eventid, priority, message, minionid):
    host_payload = {}
    host_payload['eventid'] = eventid
    host_payload['priority'] = priority
    host_payload['message'] = message
    host_payload['minion id'] = minionid

    ret = _send_server(data=host_payload)

    if ret.ok:
        return "Message sent"
    else:
        return "Error in sending message"
