

from __future__ import absolute_import
import logging

# Import Salt libs
import salt.utils
import salt.utils.compat

log = logging.getLogger(__name__)

__virtualname__ = 'win_ad'


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


def addusertogroup(username, domain, group):
    # ([adsi]"WinNT://$cname/$group,group").Add("WinNT://$cname/$user,user")

    pscmd = []
    pscmd.append(r'([adsi]"WinNT://localhost/{0},group").Add("WinNT://{1}/{2},user")'.format(
        group, domain, username))

    command = ''.join(pscmd)

    return _srvmgr(command)