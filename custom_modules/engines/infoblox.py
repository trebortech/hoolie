'''
The infoblox engine is responsible for pulling in network
information.

:configuration:

    Example configuration (master config)
        engines:
            - infoblox:
                server: 192.168.1.2
                api_version: v2.2.2
                user: admin
                password: infoblox
                sslVerify: True

:depends:
    requests
    json

'''

from __future__ import absolute_import
import logging
import time

# Import salt libs
import salt.utils

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
    return (False, 'The infoblox engine cannot start')


def start(server,
          api_version,
          user,
          password,
          sslVerify=True,
          tag='salt/engines/infoblox',
          interval=300):

    if __opts__.get('__role') == 'master':
        fire_master = salt.utils.event.get_master_event(
            __opts__,
            __opts__['sock_dir']).fire_event
    else:
        fire_master = None

    def fire(tag, msg):
        if fire_master:
            fire_master(msg, tag)
        else:
            __salt__['event.send'](tag, msg)

    # Get network
    url = 'https://{0}/wapi/{1}/network'.format(
        server,
        api_version)

    ret = requests.get(url,
                       auth=(user, password),
                       verify=sslVerify)

    if ret:
        for entry in ret.json():
            ib_network = entry['network']
            ib_ref = entry['_ref']
            ib_ds = 'sdb://infoblox/{0}'.format(ib_network)
            __salt__['sdb.set'](ib_ds, ib_ref)
            log.debug('Network: {0}'.format(ib_network))
            log.debug('REF: {0}'.format(ib_ref))

    time.sleep(interval)
