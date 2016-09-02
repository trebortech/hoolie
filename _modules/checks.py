'''
Module to manage Checks

'''

from __future__ import absolute_import
from socket import error as socket_error

# Import salt libs
import salt.utils
import logging
import time

log = logging.getLogger(__name__)

try:
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False


# Define the module's virtual name
__virtualname__ = 'checks'


def __virtual__():
    if HAS_LIBS:
        return __virtualname__

def http(name, **kwargs):

    time.sleep(5)
    for x in range(0, 10):
        try:
            data = __salt__['http.query'](name, **kwargs)
            break

        except socket_error:
            data = 'nogo'


    return data

