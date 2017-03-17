'''
Runner Module for Enterprise SaltStack management

Depends on having SaltStack Enterprise API installed


'''

from __future__ import absolute_import

import logging
import sys
import salt.client
import salt.utils.master
import json
import requests
import random


log = logging.getLogger(__name__)


def __virtual__():
    return 'eapi'


def _srvmgr(method='GET', handler=None, opts=None, data=None):

    if opts is None:
        opts = __opts__
    eapi_server = opts['sseapi_server']
    eapi_username = opts['sseapi_username']
    eapi_password = opts['sseapi_password']
    sslVerify = opts['sseapi_validate_cert']

    baseurl = '{0}'.format(eapi_server)

    conn = requests.Session()

    # Get token
    tokenurl = baseurl + '/stats'
    requesttoken = conn.get(tokenurl,
                            auth=(eapi_username, eapi_password),
                            verify=sslVerify)
    if requesttoken.status_code == 200:
        xsrftoken = requesttoken.headers['x-xsrftoken']
    else:
        return 'Error'

    headers = {}
    headers['content-type'] = 'application/json'
    headers['x-xsrftoken'] = xsrftoken

    if method == 'POST':
        eapiurl = '{0}/{1}'.format(baseurl, handler)
        requestset = conn.post(eapiurl,
                               auth=(eapi_username, eapi_password),
                               verify=sslVerify,
                               data=json.dumps(data),
                               headers=headers)
    elif method == 'GET':
        eapiurl = '{0}/{1}'.format(baseurl, handler)
        requestset = conn.get(eapiurl,
                              auth=(eapi_username, eapi_password),
                              verify=sslVerify,
                              data=json.dumps(data),
                              headers=headers)
    conn.close()

    return requestset


def copy_group(sourcegroup, newgroup):

    '''
    This will copy the permissions of one group to another
    '''

    # Make sure source exist
    source_ret = _srvmgr(method="GET", handler="auth/role")
    data_ret = json.loads(source_ret.text)['ret']
    if sourcegroup not in data_ret:
        return 'Source group does not exist'

    # Make sure new does not exist
    if newgroup in data_ret:
        return 'New group already exist'

    # Get source group permissions
    sourcegroupperms = data_ret[sourcegroup]['perms']
    # Create new group with source permissions

    data = {}
    data['name'] = newgroup
    data['perms'] = [x.encode('UTF8') for x in sourcegroupperms]
    data['desc'] = ''

    ret = _srvmgr(method="POST", handler="auth/role", data=data)

    if ret.status_code == 201:
        return "New group {0} created".format(newgroup)
    else:
        return "Error creating group"
    return True
