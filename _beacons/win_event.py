
from __future__ import absolute_import
import logging

# Import Salt libs
import salt.utils
import salt.utils.compat

LOG = logging.getLogger(__name__)

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
          win_event_interval: 10
          tag: watchmyevents
          interval: 10

    '''
    VALID_LOGS = [
        'application',
        'security',
        'system']

    VALID_TYPES = [
        'error',
        'information',
        'failureaudit',
        'successaudit',
        'warning']

    interval = config['win_event_interval']

    try:
        tag = config['tag']
    except:
        tag = 'winevent'

    ret = []

    for log in config:
        if log.lower() not in VALID_LOGS:
            return ret
        evt_config = config[log]
        # Application|Security|System

        # Entry types
        # Infomration, Error,
        entryTypes = ','.join('"' + item + '"' for item in evt_config['EntryType'])

        # Event IDs
        evtid = []

        if 'EventID' in evt_config:
            for checkid in evt_config['EventID']:
                evtid.append(r'($_.eventID -eq {0})'.format(checkid))

        if len(evtid) == 1:
            eventids = ''.join(evtid)
        elif len(evtid) > 1:
            eventids = ' -or '.join(evtid)
        else:
            eventids = ''

        pscmd = []
        pscmd.append(r'{0}'.format(entryTypes))
        pscmd.append(r'|foreach {')
        pscmd.append(r'get-eventlog ')
        pscmd.append(r'-logname {0} '.format(log))
        pscmd.append(r'-after ((get-date).addseconds(-{0})) '.format(interval))
        pscmd.append(r'-entrytype $_ ')
        pscmd.append(r'-erroraction silentlycontinue ')
        pscmd.append(r'}')
        if len(eventids) > 0:
            pscmd.append(r'|where {' + eventids + '}')
        pscmd.append(r'|fl')

        command = ''.join(pscmd)

        LOG.debug('******** POWERSHELL ***********')
        LOG.debug(command)
        retdata = _srvmgr(command)
        evData = {}
        if retdata:
            retdata = retdata.split('\r\n')
            lineitems = filter(None, retdata)
            for item in lineitems:
                try:
                    k, v = item.split(':', 1)
                    evData[k.strip()] = v.strip()
                except:
                    continue
            sub = {'tag': tag,
                   'event': evData}
            ret.append(sub)

    return ret
