

from __future__ import absolute_import
import logging

# Import Salt libs
import salt.utils
import salt.utils.compat

log = logging.getLogger(__name__)

__virtualname__ = 'win_net'


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


def add_ip(ipaddress, netmask):
    # Get a list of current ip addresses

    pscmd = []
    pscmd.append(r'get-wmiobject -class win32_networkadapterconfiguration -filter "ipenabled=true" |')
    pscmd.append(r'foreach-object{$_.IPAddress}')
    command = ''.join(pscmd)
    current_ipaddress = _srvmgr(command).split()

    if ipaddress in current_ipaddress:
        return "Address already configured"

    newipconfig = []
    newnetmask = []
    # Clear out IPV6 addresses for now
    for ip in current_ipaddress:
        if ':' not in ip:
            newipconfig.append(ip)
            newnetmask.append(netmask)

    newipconfig.append(ipaddress)
    newnetmask.append(netmask)

    ipaddress = '"' + '", "'.join(newipconfig) + '"'
    netmask = '"' + '", "'.join(newnetmask) + '"'
    pscmd = []
    pscmd.append(r'get-wmiobject -class win32_networkadapterconfiguration -filter "ipenabled=true" |')
    pscmd.append(r'foreach-object{')
    pscmd.append(r'$result = $_.enablestatic(({0}), ({1}))'.format(ipaddress, netmask))
    pscmd.append(r';$result.ReturnValue')
    pscmd.append(r'}')

    command = ''.join(pscmd)

    ret = _srvmgr(command)

    if int(ret) == 0:
        return 'Successfully added additional IP Address'
    else:
        return 'Encountered a problem'


def remove_ip(ipaddress, netmask):
    # Get a list of current ip addresses

    pscmd = []
    pscmd.append(r'get-wmiobject -class win32_networkadapterconfiguration -filter "ipenabled=true" |')
    pscmd.append(r'foreach-object{$_.IPAddress}')
    command = ''.join(pscmd)
    current_ipaddress = _srvmgr(command).split()

    if ipaddress not in current_ipaddress:
        return 'Address {0} is not configured'.format(ipaddress)

    newipconfig = []
    newnetmask = []
    # Clear out IPV6 addresses for now
    for ip in current_ipaddress:
        if ':' not in ip and ip != ipaddress:
            newipconfig.append(ip)
            newnetmask.append(netmask)

    if len(newipconfig) == 0:
        return "You can not remove the last IP Address of the machine"

    ipaddress = '"' + '", "'.join(newipconfig) + '"'
    netmask = '"' + '", "'.join(newnetmask) + '"'
    pscmd = []
    pscmd.append(r'get-wmiobject -class win32_networkadapterconfiguration -filter "ipenabled=true" |')
    pscmd.append(r'foreach-object{')
    pscmd.append(r'$result = $_.enablestatic(({0}), ({1}))'.format(ipaddress, netmask))
    pscmd.append(r';$result.ReturnValue')
    pscmd.append(r'}')

    command = ''.join(pscmd)

    ret = _srvmgr(command)

    if int(ret) == 0:
        return 'Successfully removed additional IP Address'
    else:
        return 'Encountered a problem'

