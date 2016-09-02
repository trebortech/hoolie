# Import python libs
from __future__ import absolute_import
import salt.utils


# Define the module's virtual name
__virtualname__ = 'win_ad'


def __virtual__():
    '''
    Load only on windows minions
    '''
    if salt.utils.is_windows():
        return __virtualname__
    return False


def computer_name(name):

    ret = {'name': name,
           'changes': {},
           'result': None,
           'comment': ''}

    # Change computer name
    current_name = __salt__['system.get_computer_name']()

    if current_name != name:
        ret['changes'] = {'results': 'Updated computer name'}
        newname = __salt__['system.set_computer_name'](name=name)

    ret['result'] = True

    return ret


def join_domain(name, username=None, password=None, account_ou=None,
                account_exists=False, restart=False):

    ret = {'name': name,
           'changes': {},
           'result': None,
           'comment': ''}

    domain = name
    current_domain_dic = __salt__['system.get_domain_workgroup']()

    if 'Domain' in current_domain_dic:
        current_domain = current_domain_dic['Domain']
    elif 'Workgroup' in current_domain_dic:
        current_domain = 'Workgroup'
    else:
        current_domain = None

    if domain == current_domain:
        ret['comment'] = 'Computer already added to {0}'.format(domain)

    result = __salt__['system.join_domain'](domain, username, password,
                                            account_ou, account_exists,
                                            restart)

    if result:
        ret['result'] = 'Computer added'
        ret['changes'] = {'results': 'Computer added to {0}'.format(domain)}
        ret['comment'] = 'Computer added to {0}'.format(domain)
    else:
        ret['comment'] = 'Computer failed to join {0}'.format(domain)
        ret['result'] = False

    return ret


def groupadd(name, domain, group):

    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': ''}
    user = name

    ret_data = __salt__['win_ad.addusertogroup'](user, domain, group)

    if len(ret_data) > 0:
        if "already a member" in ret_data:
            ret['comment'] = '{0} is already a member of group {1}'.format(user, group)
        elif "group name could not be found" in ret_data:
            ret['comment'] = '{0} does not exist on this machine'.format(group)
            ret['result'] = False
        else:
            ret['comment'] = 'An unknown error has occured'
            ret['result'] = False
    else:
        ret['changes'] = {'results': '{0} has been added to {1}'.format(user, group)}
        ret['comment'] = '{0} has been added to {1}'.format(user, group)

    return ret
