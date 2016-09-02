# -*- coding: utf-8 -*-
'''
Module to help with application deployments

'''


from __future__ import absolute_import


# Import salt libs
import salt.utils

# Define the module's virtual name
__virtualname__ = 'appctl'


def __virtual__():
    return __virtualname__


def deploy(appname, newversion):

    pil = {"version": newversion}

    # put into Maintenance mode

    zenosstag = 'zenoss/prodstate/set'
    inmaint = {"prod_state": "Maintenance"}

    __salt__['event.fire_master'](
        data=inmaint,
        tag=zenosstag
    )

    ret = __salt__['state.sls'](
        mods='sites.{0}'.format(appname),
        pillar=pil
    )

    # Log message to Zenoss that software was updated

    zenosseventtag = 'zenoss/event'
    zenossevent = {"message": appname + " was updated to version " + newversion}
    __salt__['event.fire_master'](
        data=zenossevent,
        tag=zenosseventtag
    )

    # Take out of Maintenance mode

    outmaint = {"prod_state": __grains__['prod_state']}

    __salt__['event.fire_master'](
        data=outmaint,
        tag=zenosstag
    )

    ret = "{0} has been updated to version {1}".format(appname, newversion)
    return ret
