# -*- coding: utf-8 -*-
'''
Beacon to monitor file contents change.

'''

# Import Python libs
from __future__ import absolute_import
import logging
import os
import mmap

# Import Salt libs
import salt.utils

log = logging.getLogger(__name__)

__virtualname__ = 'filecheck'


def __virtual__():
    if salt.utils.is_windows():
        return False
    else:
        return __virtualname__


def validate(config):
    '''
    Validate the beacon configuration
    '''
    # Configuration for diskusage beacon should be a list of dicts
    if not isinstance(config, dict):
        log.info('Configuration for filecheck beacon must be a dictionary.')
        return False
    return True


def beacon(config):
    '''
    Check file for value certain value

    .. code-block:: yaml

        beacons:
          filecheck:
            /var/log/test:
              alerton:
                - 'service down'
                - error
              interval: 5
            /var/log/test2:
              alerton:
                - 'service down'
                - running
              interval: 5
    '''
    ret = []
    DEFAULT_ALERT = ['error']

    import pprint
    log.debug(pprint.pprint(config))
    for path in config:
        log.debug('checking ' + path)
        if isinstance(config[path], dict):
            # Valid python dict
            alerton = config[path].get('alerton', DEFAULT_ALERT)
        else:
            alerton = DEFAULT_ALERT
        # Check file for alert contents

        # Check if file exist
        if os.path.isfile(path) and os.stat(path).st_size > 0:
            f = open(path)
            filesocket = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            for check4this in alerton:
                if filesocket.find(check4this) != -1:
                    sub = {'tag': path,
                           'contains': check4this}
                    ret.append(sub)
        else:
            sub = {'tag': path,
                   'contains': 'file does not exist or is empty'}
            ret.append(sub)

    return ret
