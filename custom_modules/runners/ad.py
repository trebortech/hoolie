'''
Runner Module for AD User/Group management

Depends on grain value being set for activedirectory server


'''

from __future__ import absolute_import

import logging
import salt.client
import salt.utils.master
import random

log = logging.getLogger(__name__)


def __virtual__():
    return 'ad'


def _srvmgr(func):

    adhost = _get_ad_server()
    myargs = []
    salt_cmd = 'cmd.run'
    myargs.append('Import-Module activedirectory; {0}'.format(func))
    myargs.append('shell=powershell')
    myargs.append('python_shell=True')

    local = salt.client.get_local_client(__opts__['conf_file'])
    cmd_ret = local.cmd('{0}'.format(adhost), salt_cmd, myargs)

    if len(cmd_ret) == 0:
        log.error('Unable to execute command: %s', func)

    return cmd_ret[adhost]


def _get_pillar_cache():

    tgt = 'saltmaster'
    expr_form = 'glob'

    pillar_util = salt.utils.master.MasterPillarUtil(
        tgt,
        expr_form,
        use_cached_grains=True,
        grains_fallback=False,
        opts=__opts__)

    return pillar_util.get_minion_pillar()


def _get_ad_server():
    # Get a list of minions that have the AD role
    # Randomly select one of them

    adhost = []

    tgt = 'activedirectory:True'
    expr_form = 'grain'

    pillar_util = salt.utils.master.MasterPillarUtil(
        tgt,
        expr_form,
        use_cached_grains=True,
        grains_fallback=False,
        opts=__opts__)

    cached_grains = pillar_util.get_minion_grains()

    for item in cached_grains.viewitems():
        if len(item[1]) > 0:
            adhost.append(item[0])

    return random.choice(adhost)


def get_allusers():
    command = 'get-aduser -filter * | select name'
    ret_names = _srvmgr(command).split()

    names = []
    for name in ret_names:
        if name not in ('name', '----'):
            names.append(name)
    return names


def get_user(name):
    command = "get-aduser -filter 'Name -like \"{0}\"' | select name".format(name)
    ret_names = _srvmgr(command).split()

    names = []
    for name in ret_names:
        if name not in ('name', '----'):
            names.append(name)
    return names


def remove_users(
        pillarkey,
        saltmaster='saltmaster'):

    cached_pillars = _get_pillar_cache()

    ret = []
    for user in cached_pillars[saltmaster][pillarkey]:

        username = user['name']

        if len(get_user(username)) == 0:
            return "User {0} does not exists".format(username)

        pscmd = []
        pscmd.append('remove-aduser')
        pscmd.append('-Identity {0}'.format(username))
        pscmd.append('-Confirm:$false')

        command = ' '.join(pscmd)

        ret_data = _srvmgr(command)
        if len(ret_data) == 0:
            ret.append('User {0} removed successfully'.format(username))
        else:
            ret.append('Encountered a problem removing user account\n{0}'.format(ret_data))

    return '\n'.join(ret)


def create_users(
        pillarkey,
        saltmaster='saltmaster'):

    # Check to see if user already exists

    cached_pillars = _get_pillar_cache()

    ret = []

    for user in cached_pillars[saltmaster][pillarkey]:

        username = user['name']
        domain = user['domain']
        password = user['password']

        if len(get_user(username)) > 0:
            return "User {0} already exists".format(username)

        pscmd = []
        pscmd.append('new-aduser')
        pscmd.append('-SamAccountName {0}'.format(username))
        pscmd.append('-Name {0}'.format(username))
        pscmd.append('-UserPrincipalName {0}@{1}'.format(username, domain))
        pscmd.append('-AccountPassword (ConvertTo-SecureString {0} -AsPlainText -Force)'.format(password))
        pscmd.append('-Enabled $true')
        pscmd.append('-PasswordNeverExpires $true')

        command = ' '.join(pscmd)

        ret_data = _srvmgr(command)
        if len(ret_data) == 0:
            ret.append('User {0} created successfully'.format(username))
        else:
            ret.append('Encountered a problem creating user account\n{0}'.format(ret_data))

    return '\n'.join(ret)


def add_usertogroup(
        pillarkey,
        saltmaster='saltmaster'):

    cached_pillars = _get_pillar_cache()

    ret = []

    for user in cached_pillars[saltmaster][pillarkey]:
        username = user['name']
        groups = user['groups']

        if type(groups) is list:
            for group in groups:
                pscmd = []
                pscmd.append('add-adgroupmember')
                pscmd.append('{0}'.format(group))
                pscmd.append('-members {0}'.format(username))

                command = ' '.join(pscmd)
                ret_data = _srvmgr(command)

                if len(ret_data) > 0:
                    ret.append('Encountered a problem adding user to group\n{0}'.format(ret_data))
                else:
                    ret.append('User {0} was successfully added to group {1}'.format(username, group))

        elif type(groups) is str:
            pscmd = []
            pscmd.append('add-adgroupmember')
            pscmd.append('{0}'.format(groups))
            pscmd.append('-members {0}'.format(username))

            command = ' '.join(pscmd)
            ret_data = _srvmgr(command)

            if len(ret_data) > 0:
                ret.append('Encountered a problem adding user to group\n{0}'.format(ret_data))
            else:
                ret.append('User {0} was successfully added to group {1}'.format(username, groups))

    return '\n'.join(ret)


def get_group(groupname):

    command = "get-adgroup -filter 'Name -like \"{0}\"' | select name".format(groupname)
    ret_names = _srvmgr(command).split()

    names = []
    for name in ret_names:
        if name not in ('name', '----'):
            names.append(name)
    return names


def remove_secgroups(
        pillarkey,
        saltmaster='saltmaster'):

    cached_pillars = _get_pillar_cache()

    ret = []
    for groups in cached_pillars[saltmaster][pillarkey]:

        groupname = groups['name']
        if len(get_group(groupname)) == 0:
            ret.append("Security Group {0} does not exists".format(groupname))
        else:
            pscmd = []
            pscmd.append('remove-adgroup')
            pscmd.append('-Identity {0}'.format(groupname))
            pscmd.append('-Confirm:$false')

            command = ' '.join(pscmd)
            ret_data = _srvmgr(command)

            if 'group does not exists' in ret_data:
                ret.append('Group {0} already removed'.format(groupname))
            elif len(ret_data) > 0:
                ret.append('Encountered a problem removing group \n{0}'.format(ret_data))
            else:
                ret.append('Group {0} was successfully removed'.format(groupname))

    return '\n'.join(ret)


def create_secgroups(
        pillarkey,
        saltmaster='saltmaster',
        groupscope='Global',
        path=None):

    cached_pillars = _get_pillar_cache()

    ret = []
    for groups in cached_pillars[saltmaster][pillarkey]:

        groupname = groups['name']
        if len(get_group(groupname)) > 0:
            ret.append("Security Group {0} already exists".format(groupname))
        else:
            pscmd = []
            pscmd.append('new-adgroup')
            pscmd.append('-name {0}'.format(groupname))
            pscmd.append('-GroupScope {0}'.format(groupscope))
            if path:
                pscmd.append('-Path {0}'.format(path))

            command = ' '.join(pscmd)
            ret_data = _srvmgr(command)

            if 'group already exists' in ret_data:
                ret.append('Group {0} already exists'.format(groupname))
            elif len(ret_data) > 0:
                ret.append('Encountered a problem creating group \n{0}'.format(ret_data))
            else:
                ret.append('Group {0} was successfully created'.format(groupname))

    return '\n'.join(ret)


def unjoin_domain(computers):

    ret_data = []
    for computer in computers:
        pscmd = []
        pscmd.append('remove-adcomputer -identity {0} -confirm:$false'.format(computer))
        command = ''.join(pscmd)
        ret = _srvmgr(command)
        if 'Cannot find' in ret:
            ret_data.append('Could not find computer {0}'.format(computer))
        elif len(ret) == 0:
            ret_data.append('Computer {0} removed'.format(computer))

    return '\n'.join(ret_data)
