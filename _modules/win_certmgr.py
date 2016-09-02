# -*- coding: utf-8 -*-
'''
Microsoft Certificate manager

:platform:      Windows

.. versionadded:: Boron

NOTES: https://blogs.technet.microsoft.com/scotts-it-blog/2014/12/30/working-with-certificates-in-powershell/

'''


from __future__ import absolute_import


# Import salt libs
import salt.utils

# Define the module's virtual name
__virtualname__ = 'win_certmgr'


def __virtual__():
    '''
    Load only on Windows
    '''
    if salt.utils.is_windows():
        return __virtualname__
    return False


def _srvmgr(func):
    '''
    Execute a function from the PKI PS module
    '''

    return __salt__['cmd.run'](
        'Import-Module PKI; {0}'.format(func),
        shell='powershell',
        python_shell=True)


def list_certstores(location):
    '''
    List all the currently deployed certificates

    CLI Example:

    .. code-block:: bash

        salt '*' win_certmgr.list_certstores location='LocalMachine'
    '''
    pscmd = []
    pscmd.append(r'set-location CERT:\{0};'.format(location))
    pscmd.append(r'Get-ChildItem')
    pscmd.append(r' | foreach {')
    pscmd.append(r' $_.Name')
    pscmd.append(r'};')

    command = ''.join(pscmd)
    return _srvmgr(command)


def view_certfile(certpath):

    pscmd = []
    pscmd.append(r'$cert = new-object system.security.cryptography.x509certificates.x509certificate2;')
    pscmd.append(r'$cert.import("{0}");'.format(certpath))
    pscmd.append(r'$cert.Subject')

    command = ''.join(pscmd)
    return _srvmgr(command)


def list_certs(location, datastore):

    pscmd = []
    pscmd.append(r'set-location CERT:\{0}\{1};'.format(location, datastore))
    pscmd.append(r'Get-ChildItem')
    pscmd.append(r' | foreach {')
    pscmd.append(r' $_.Subject')
    pscmd.append(r'};')

    command = ''.join(pscmd)
    return _srvmgr(command)


def add_cert(location, datastore, certpath, pfx=False):

    pscmd = []
    pscmd.append(r'get-childitem -path {0} |'.format(certpath))
    if pfx:
        pscmd.append(r'import-pfxcertificate -certstorelocation CERT:\{0}\{1};'.format(location, datastore))       
    else:
        pscmd.append(r'import-certificate -certstorelocation CERT:\{0}\{1};'.format(location, datastore))

    command = ''.join(pscmd)
    return _srvmgr(command)


def add_crl(datastore, crlpath):
    pscmd = []
    pscmd.append(r'certutil -addstore -f {0} {1}'.format(datastore, crlpath))

    command = ''.join(pscmd)
    return _srvmgr(command)


def create_cert_binding(name, site, hostheader='', ipaddress='*', port=443, sslflags=0,
        location=None, datastore=None, certhash=None):

    pscmd = []
    pscmd.append(r'New-WebBinding -Name "{0}" -IP "*" -Port {2} -Protocol https;'.format(
        site,
        ipaddress,
        port))

    pscmd.append(r'cd IIS:\sslbindings;')
    pscmd.append(r'get-item cert:\{0}\{1}\{2} | new-item *!{4}'.format(
        location,
        datastore,
        certhash,
        ipaddress,
        port))


    command = ''.join(pscmd)
    return _srvmgr(command)