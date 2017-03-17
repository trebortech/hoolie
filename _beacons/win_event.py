
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
            Failed Logins:   <--- Descriptive Name
              eventlog: Security   <--- Event lob to watch
              entrytype: failureaudit  <--- Event Type
              eventid: 4625    <--- Event ID
              tag: 'failed login'  <--- Custom event tag
            App failure:  
              eventlog: Application
              entrytype:
                - Error
                - Information
              eventid:
                - 12
                - 234
                - 567
              tag: 'App 1 failed'
          win_event_interval: 10  <--- Length of time to look back at events
          tag: watchmyevents <--- Default tag for event. Used if not specified above
          interval: 10  <--- Beacon run interval

    '''
    # Settings in config to ignore
    IGNORE_TYPES = [
        'win_event_interval',
        'interval']

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

    for check in config:
        if check in IGNORE_TYPES:
            continue

        # check is the descritive name of the check
        evt_config = config[check]

        eventlog = evt_config.get('eventlog', '')
        entrytypes = evt_config.get('entrytype', '')
        eventid = evt_config.get('eventid', '')
        tag = evt_config.get('tag', tag)

        evtid = []
        enttype = []

        if isinstance(entrytypes, list):
            for entrytype in entrytypes:
                enttype.append(r'"' + entrytype + '"')
        else:
            enttype.append(r'"' + entrytypes + '"')

        enttypes = ','.join(enttype)

        if isinstance(eventid, list):
            for eid in eventid:
                evtid.append(r'($_.eventID -eq {0})'.format(eid))
        elif isinstance(eventid, str):
            evtid.append(r'($_.eventID -eq {0})'.format(eventid))

        if len(evtid) == 1:
            eventids = ''.join(evtid)
        elif len(evtid) > 1:
            eventids = ' -or '.join(evtid)
        else:
            eventids = ''

        pscmd = []
        pscmd.append(r'{0}'.format(enttypes))
        pscmd.append(r'|foreach {')
        pscmd.append(r'get-eventlog ')
        pscmd.append(r'-logname {0} '.format(eventlog))
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
