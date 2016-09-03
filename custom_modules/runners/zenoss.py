# -*- coding: utf-8 -*-
'''
Runner Module for Interacting with Zenoss

:configuration: This module can be used by specifying the name of a
    configuration profile in the master config.

    For example:

    .. code-block:: yaml

        zenoss:
            hostname: https://zenoss.example.com
            username: admin
            password: admin123
'''
from __future__ import absolute_import

# Import python libs
import json
import logging
import re

# Import salt libs

try:
    import requests
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False

log = logging.getLogger(__name__)

ROUTERS = {'MessagingRouter': 'messaging',
           'EventsRouter': 'evconsole',
           'ProcessRouter': 'process',
           'ServiceRouter': 'service',
           'DeviceRouter': 'device',
           'NetworkRouter': 'network',
           'TemplateRouter': 'template',
           'DetailNavRouter': 'detailnav',
           'ReportRouter': 'report',
           'MibRouter': 'mib',
           'ZenPackRouter': 'zenpack'}

PROD_STATES = {'Production': 1000,
               'Pre-Production': 500,
               'Test': 400,
               'Maintenance': 300,
               'Decommissioned': -1}


def __virtual__():
    '''
    Only load if requests is installed
    '''
    if HAS_LIBS:
        return 'zenoss'


def _session():
    '''
    Create a session to be used when connecting to Zenoss.
    '''

    config = __opts__.get('zenoss', None)
    session = requests.session()
    session.auth = (config.get('username'), config.get('password'))
    session.verify = False
    session.headers.update({'Content-type': 'application/json; charset=utf-8'})
    return session


def _http_get(page, data=None):
    '''
    Make a normal http get to Zenoss
    '''

    config = __opts__.get('zenoss', None)

    if config is None:
        log.debug('No zenoss configurations found in master config')
        return False
    else:
        url = '{0}/zport/dmd/{1}?{2}'.format(config.get('hostname'),
                                             page,
                                             data)
        response = _session().get(url)

    return response.ok


def _http_post(page, data=None):
    '''
    Make a normal http post to Zenoss
    '''

    config = __opts__.get('zenoss', None)

    if config is None:
        log.debug('No zenoss configurations found in master config')
        return False
    else:
        url = '{0}/zport/dmd/{1}'.format(config.get('hostname'),
                                         page)
        data = json.dumps(data)
        response = _session().post(url, data)

    return response.ok


def _router_request(router, method, data=None):
    '''
    Make a request to the Zenoss API router
    '''
    if router not in ROUTERS:
        return False

    req_data = json.dumps([dict(
        action=router,
        method=method,
        data=data,
        type='rpc',
        tid=1)])

    config = __opts__.get('zenoss', None)
    log.debug('Making request to router %s with method %s', router, method)
    url = '{0}/zport/dmd/{1}_router'.format(config.get('hostname'), ROUTERS[router])
    response = _session().post(url, data=req_data)

    # The API returns a 200 response code even whe auth is bad.
    # With bad auth, the login page is displayed. Here I search for
    # an element on the login form to determine if auth failed.
    if re.search('name="__ac_name"', response.content):
        log.error('Request failed. Bad username/password.')
        raise Exception('Request failed. Bad username/password.')

    return json.loads(response.content).get('result', None)


def _get_all_devices():
    data = [{'uid': '/zport/dmd/Devices', 'params': {}, 'limit': None}]
    all_devices = _router_request('DeviceRouter', 'getDevices', data=data)
    return all_devices


def find_device(device=None):
    '''
    Find a device in Zenoss. If device not found, returns None.

    Parameters:
        device:         (Required) The device name in Zenoss

    CLI Example:
        salt-run zenoss.find_device device=saltmaster
    '''
    all_devices = _get_all_devices()
    for dev in all_devices['devices']:
        if dev['name'] == device:
            # We need to save the hash for later operations
            dev['hash'] = all_devices['hash']
            log.info('Found device %s in Zenoss', device)
            return dev

    log.info('Unable to find device %s in Zenoss', device)
    return False


def device_exists(device=None):
    '''
    Check to see if a device already exists in Zenoss.

    Parameters:
        device:         (Required) The device name in Zenoss

    CLI Example:
        salt-run zenoss.device_exists device=saltmaster
    '''
    if find_device(device):
        return True
    return False


def add_device(deviceName,
               deviceClass,
               title=None,
               snmpCommunity='',
               snmpPort=161,
               manageIp="",
               model=True,
               collector='localhost',
               rackSlot=0,
               locationPath="",
               systemPaths=[],
               groupPaths=[],
               prod_state='Production',
               comments="",
               hwManufacturer="",
               hwProductName="",
               osManufacturer="",
               osProductName="",
               priority=3,
               tag="",
               serialNumber="",
               zCommandUsername="",
               zCommandPassword="",
               zWinUser="",
               zWinPassword="",
               zProperties={},
               cProperties={}):
    '''
    A function to connect to a zenoss server and add a new device entry.

    Parameters:
        deviceName:     (Required) The device name in Zenoss
        deviceClass:    (Required) The device class to use. If none, will determine based on kernel grain.
        prod_state:     (Optional)(Default Production) The prodState to set on the device.
        title:          (Optional) See Zenoss documentation
        snmpCommunity:  (Optional) See Zenoss documentation
        snmpPort:       (Optional) See Zenoss documentation
        manageIp:       (Optional) See Zenoss documentation
        model:          (Optional) See Zenoss documentation
        collector:      (Optional)(Default localhost) The collector to use for this device.
        rackSlot:       (Optional) See Zenoss documentation
        locationPath:   (Optional) See Zenoss documentation
        systemPaths:    (Optional) See Zenoss documentation
        groupPaths:     (Optional) See Zenoss documentation
        prod_state:     (Optional) See Zenoss documentation
        comments:       (Optional) See Zenoss documentation
        hwManufacturer: (Optional) See Zenoss documentation
        hwProductName:  (Optional) See Zenoss documentation
        osManufacturer: (Optional) See Zenoss documentation
        osProductName:  (Optional) See Zenoss documentation
        priority:       (Optional) See Zenoss documentation
        tag:            (Optional) See Zenoss documentation
        serialNumber:   (Optional) See Zenoss documentation
        zCommandUsername: (Optional) See Zenoss documentation
        zCommandPassword: (Optional) See Zenoss documentation
        zWinUser:       (Optional) See Zenoss documentation
        zWinPassword:   (Optional) See Zenoss documentation
        zProperties:    (Optional) See Zenoss documentation
        cProperties:    (Optional) See Zenoss documentation

    CLI Example:
        salt-run zenoss.add_device deviceName=saltmaster deviceClass='/Server/Linux'
    '''

    if device_exists(deviceName):
        return 'Device already exists'

    log.info('Adding device %s to zenoss', deviceName)

    data = dict(deviceName=deviceName,
                deviceClass=deviceClass,
                title=title,
                snmpCommunity=snmpCommunity,
                snmpPort=snmpPort,
                manageIp=manageIp,
                model=model,
                collector=collector,
                rackSlot=rackSlot,
                locationPath=locationPath,
                systemPaths=systemPaths,
                groupPaths=groupPaths,
                productionState=PROD_STATES[prod_state],
                comments=comments,
                hwManufacturer=hwManufacturer,
                hwProductName=hwProductName,
                osManufacturer=osManufacturer,
                osProductName=osProductName,
                priority=priority,
                tag=tag,
                serialNumber=serialNumber,
                zCommandUsername=zCommandUsername,
                zCommandPassword=zCommandPassword,
                zWinUser=zWinUser,
                zWinPassword=zWinPassword,
                zProperties=zProperties,
                cProperties=cProperties)

    response = _router_request('DeviceRouter', 'addDevice', data=[data])
    return response


def set_prod_state(prod_state, device=None):
    '''
    A function to set the prod_state in zenoss.

    Parameters:
        prod_state:     (Required) String value of the state
                        - Production
                        - Pre-Production
                        - Test
                        - Maintenance
                        - Decommissioned

        device:         (Required) The device name in Zenoss

    CLI Example:
        salt-run zenoss.set_prod_state prod_state=1000 device=saltmaster
    '''

    device_object = find_device(device)

    if not device_object:
        return "Unable to find a device in Zenoss for {0}".format(device)

    log.info('Setting prodState to %d on %s device', prod_state, device)
    data = dict(uids=[device_object['uid']], prodState=PROD_STATES[prod_state], hashcheck=device_object['hash'])
    return _router_request('DeviceRouter', 'setProductionState', [data])


def get_decomm():
    '''
    A function to get all decommissioned devices in Zenoss.

    CLI Example:
        salt-run zenoss.get_decomm

    '''

    log.info('Get all decommissioned devices from Zenoss')

    decomm_device = []
    all_devices = _get_all_devices()
    for dev in all_devices['devices']:
        if dev['productionState'] == PROD_STATES['Decommissioned']:
            decomm_device.append(dev['name'])

    if decomm_device.__len__() > 0:
        return decomm_device
    else:
        return 'No devices returned'
        log.info(dev['hash'])

    return True


def send_event(summary, device, severity, evclasskey=None, evclass=None, component=None):
    '''
    A function to send events to Zenoss

    Parameters:
        summary:        (Required) The summary of the event
        device:         (Required) The device name in Zenoss
        severity:       (Required) String value of the state
                        - Critical
                        - Error
                        - Warning
                        - Info
                        - Debug
                        - Clear
        evclasskey:     (optional) The Event class key from Zenoss
        evclass:        (optional) The Event class for the event
        component:      (optional) The component on the device this message refers to

    CLI Example:
        salt-run zenoss.send_event summary='Config just executed' device=saltmaster severity='Info'
    '''

    data = [{
        'summary': summary,
        'device': device,
        'component': component,
        'severity': severity,
        'evclasskey': evclasskey,
        'evclass': evclass}]
    ret = _router_request('EventsRouter', 'add_event', data=data)

    return ret


def add_user(username, email):

    data = []
    data.append('tableName=userlist')
    data.append('zenScreenName=manageUserFolder.pt')
    data.append('filter=""')
    data.append('userid=' + username)
    data.append('email=' + email)
    data.append('manage_addUser:method=OK')

    data = '&'.join(data)
    ret = _http_get('ZenUsers', data=data)

    return ret


def reset_password(username):

    data = []
    data.append('manage_resetPassword:method=Submit')

    ret = _http_post('ZenUsers/' + username, data=data)

    return ret


def update_password(username, password):

    config = __opts__.get('zenoss', None)

    data = []
    data.append('roles:list=ZenUser')
    #data.append('email=mywebtest2@saltstack.com')
    #data.append('pager=')
    #data.append('defaultPageSize=40')
    #data.append('defaultAdminRole=ZenUser')
    #data.append('netMapStartObject=')
    data.append('password=' + password)
    data.append('sndpassword=' + password)
    data.append('oldpassword=' + config.get('password'))
    data.append('manage_editUserSettings:method=+Save+Settings+')

    data = '&'.join(data)
    ret = _http_get('ZenUsers/' + username, data=data)

    return ret
