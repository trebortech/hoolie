'''
ElasticSearch Shield security plugin
'''

from __future__ import absolute_import
from socket import error as socket_error

# Import salt libs
import salt.utils
import logging
import yaml

log = logging.getLogger(__name__)

shieldconfig = '/etc/elasticsearch/shield/'
esusers = '/usr/share/elasticsearch/bin/shield/esusers '

try:
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False


# Define the module's virtual name
__virtualname__ = 'shield'


def __virtual__():
    if HAS_LIBS:
        return __virtualname__


def _yaml(docstring):

    docs = []
    try:
        docs.append(yaml.load(docstring))
    except SyntaxError:
        docs.append(docstring)

    return docs

def _srvmgr(func):
    '''
    Execute a function from the WebAdministration PS module
    '''

    return __salt__['cmd.run'](func)


def list_roles():

    roles = open(shieldconfig + 'roles.yml', 'r').read()

    roles = _yaml(roles)
    rolelist = roles[0].keys()
    return rolelist

def list_users():
    
    users = _srvmgr(esusers + 'list').split('\n')

    dct = {}
    for user in users:
        line = user.split(':')
        dct[line[0].strip()] = line[1].strip()

    return dct


def user_exists(username):

    users = list_users()

    if username in users:
        return True
    else:
        return False


def user_add(username, password, roles=None):

    cmd = []
    cmd.append('useradd ')
    cmd.append(username)
    cmd.append('-p {0}'.formadt(password))
    if roles:
        availroles = list_roles()
        rolelist = roles.split(',')
        for role in rolelist:
            if role not in availroles:
                return role + " is invalid role"

        cmd.append('-r {0}'.format(roles))
    command = ' '.join(cmd)
    return _srvmgr(esusers + command)

def user_mod(username, password=None, rroles=None, aroles=None):

    cmd = []
    
    if password:
        cmd.append('passwd')
        cmd.append(username)
        cmd.append('-p {0}'.format(password))
        command = ' '.join(cmd)
        _srvmgr(esusers + command)

    if rroles or aroles:
        availroles = list_roles()
        cmd = []
        cmd.append('roles ')
        cmd.append(username)
    
        if rroles:
            rolelist = rroles.split(',')
            for role in rolelist:
                if role not in availroles:
                    return role + " is invalid role"
            cmd.append('-r {0}'.format(rroles))

        if aroles:
            rolelist = aroles.split(',')
            for role in rolelist:
                if role not in availroles:
                    return role + " is invalid role"
            cmd.append('-a {0}'.format(aroles))

        command = ' '.join(cmd)
        _srvmgr(esusers + command)

    return True