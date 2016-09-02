'''
Windows Service Management
'''

# Import python libs
import logging
import re

# Import salt libs
import salt.utils

log = logging.getLogger(__name__)


# Define the module's virtual name
__virtualname__ = 'win_service'

def __virtual__():
    '''
    Only works on Windows systems
    '''
    if salt.utils.is_windows():
        return __virtualname__
    return False

def stop(name):
    # Stop service
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': ''}

    __salt__['service.stop'](name)

    ret['comment'] = "{0} service stopped".format(name)
    return ret


def start(name):

    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': ''}

    __salt__['service.start'](name)

    ret['comment'] = "{0} service started".format(name)
    return ret