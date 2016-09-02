'''
Updates from events

'''
import logging

# Import salt libs
import salt.utils

log = logging.getLogger(__name__)

try:
    import RPi.GPIO as GPIO
    import pyttsx
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False

# Define the module's virtual name
__virtualname__ = 'zenny'


def __virtual__():
    if HAS_LIBS:
        return __virtualname__


def alert(name, color, message):

    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': ''}

    __salt__['zenny.statusupdate'](color=color)
    __salt__['zenny.say'](msg=message)

    ret['comment'] = 'Message was sent to Zenny'

    return ret
