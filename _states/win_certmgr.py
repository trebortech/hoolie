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
__virtualname__ = 'win_certmgr'


def __virtual__():
    '''
    Only works on Windows systems
    '''
    if salt.utils.is_windows():
        return __virtualname__
    return False


def cert_installed(name, location, datastore, certpath, pfx=False):
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': ''}

    # Get the cert subject

    certsubject = __salt__['win_certmgr.view_certfile'](certpath)

    # Get a list of cert subject installed

    certlist = __salt__['win_certmgr.list_certs'](location, datastore)

    # check to see if cert is already installed

    if certsubject in certlist:
        ret['comment'] = "{0} is already installed".format(certsubject)

    else:
        addcert = __salt__['win_certmgr.add_cert'](location, datastore, certpath, pfx)
        ret['result'] = True
        ret['changes'] = {'results': '{0}'.format(addcert)}
        ret['comment'] = "{0} has been installed".format(certsubject)

    return ret


def crl_installed(name, datastore, crlpath):

    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': ''}

    addcrl = __salt__['win_certmgr.add_crl'](datastore, crlpath)

    if "already in store" in addcrl:
        ret['result'] = True
        ret['comment'] = "{0} was already installed".format(crlpath)
    else:
        ret['result'] = True
        ret['changes'] = {'results': '{0}'.format(addcrl)}
        ret['comment'] = "{0} has been installed".format(crlpath)
    return ret

def create_cert_binding(name,
                        site,
                        hostheader='',
                        ipaddress='*',
                        port=443,
                        sslflags=0,
                        location=None,
                        datastore=None,
                        certhash=None):

    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': ''}      

    ret_data = __salt__['win_certmgr.create_cert_binding'](
        name, site, hostheader, ipaddress, port, sslflags,
        location, datastore, certhash)

    ret['result'] = ret_data

    return ret