

from __future__ import absolute_import
import logging

# Import Salt libs
import salt.utils
import salt.utils.compat

log = logging.getLogger(__name__)

__virtualname__ = 'win_disk'


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


def initialize_disk(driveletter):
    # Get a list of current ip addresses

    pscmd = []
    pscmd.append(r'$h="{0}";'.format(driveletter))
    pscmd.append(r'$disk=get-disk | where-object isoffline -eq $true;')
    pscmd.append(r'$disk | set-disk -isoffline $false;')
    pscmd.append(r'initialize-disk $disk.Number;')
    pscmd.append(r'new-partition -disknumber $disk.Number -usemaximumsize -driveletter $h;')
    pscmd.append(r'format-volume -driveletter $h -Confirm:$false;')
    command = ''.join(pscmd)

    ret = _srvmgr(command)

    '''
    if int(ret) == 0:
        return 'Successfully added additional disk as drive letter {0}'.format(driveletter)
    else:
        return 'Encountered a problem'
    '''
    return ret