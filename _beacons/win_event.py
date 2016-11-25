
from __future__ import absolute_import
import logging

# Import Salt libs
import salt.utils
import salt.utils.compat

log = logging.getLogger(__name__)

__virtualname__ = 'win_event'


def __virtual__():
    '''
    Load only on Windows
    '''
    if salt.utils.is_windows():
        return __virtualname__
    return False


def _srvmgr(func):
    '''
    Execute a function from the WebAdministration PS module
    '''

    return __salt__['cmd.run'](
        '{0}'.format(func),
        shell='powershell',
        python_shell=True)


def beacon(config):

    '''

    Example Config
        beacons:
          win_event:
            Application:
              EntryType:
                - Error
            Security:
              EntryType:
                - information
              EventID:
                - 902
          interval: 10

    '''
    VALID_LOGS = [
        'application',
        'security',
        'system']

    VALID_TYPES = [
        'error',
        'information']

    interval = config['interval']
    ret = []

    for log in config:
        evt_config = config[log]
        # Application|Security|System

        # Entry types
        # Infomration, Error, ...
        entryTypes = ','.join(evt_config['EntryType'])

        # Event IDs
        evtid = []
        for checkid in evt_config['EventID']:
            evtid.append(r'($_.eventID -eq {0})'.format(checkid))

        if len(evtid) == 1:
            eventids = evtid
        elif len(evtid) > 1:
            eventids = ' -or '.join(evtid)
        else:
            eventids = []

        pscmd = []
        pscmd.append(r'{0}'.format(entryTypes))
        pscmd.append(r'|foreach {')
        pscmd.append(r'get-eventlog ')
        pscmd.append(r'-logname {0}'.format(log))
        pscmd.append(r'-after ((get-date).addseconds(-{0}))'.format(interval))
        pscmd.append(r'-entrytype $_')
        pscmd.append(r'-erroraction silentlycontinue')
        pscmd.append(r'}')
        if len(eventids) > 0:
            pscmd.append(r'|where {{0}}'.format(eventids))
        pscmd.append(r'|fl')

        command = ''.join(pscmd)

        log.debug('******** POWERSHELL ***********')
        log.debug(command)

        retdata = _srvmgr(command)

        ret.append(retdata)

    return ret
