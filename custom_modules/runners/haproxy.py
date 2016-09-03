

from __future__ import absolute_import

import logging
import random
import time

# Import Salt libs
import salt.utils
import salt.client
import salt.utils.master
import salt.utils.compat

try:
    # pylint: disable=unused-import
    import boto
    from boto.ec2 import EC2Connection as ec2
    # pylint: enable=unused-import
    HAS_BOTO = True
except ImportError:
    HAS_BOTO = False


log = logging.getLogger(__name__)


def __virtual__():
    if not HAS_BOTO:
        return (False, "The boto_ec2 module cannot be loaded: boto library not found")
    else:
        return True


def set_secondary_ip(minion, aws=False, newip=''):

    if aws:
        config = __opts__.get('aws', None)
        key = config.get('key')
        keyid = config.get('keyid')

        secondary_count=1

        ec2conn = ec2(keyid, key)

        # Get HAProxy Instance
        reservations = ec2conn.get_all_instances(filters={'tag:Name': '{0}'.format(minion)})
        # Get eni id from haproxy
        instance = reservations[0].instances[0]
        interface_id = instance.interfaces[0].id
        try:
            ret_data = ec2conn.assign_private_ip_addresses(
                network_interface_id=interface_id,
                secondary_private_ip_address_count=secondary_count)

        except boto.exception.BotoServerError as e:
            log.error(e)
            return 'Error occured {0}'.format(e)

        # put in wait for AWS to do it's thing
        time.sleep(5)
        # Get what IP was assigned

        newinterface = ec2conn.get_all_network_interfaces(interface_id)
        ipaddresses = newinterface[0].private_ip_addresses

        for ip in ipaddresses:
            if ip.primary is False:
                newip = ip.private_ip_address

    # Update HAProxy config with new IP

    local = salt.client.get_local_client(__opts__['conf_file'])

    salt_cmd = 'cmd.run'
    myargs = []
    myargs.append('ip addr add dev eth0 {0}/24'.format(newip))
    cmd_ret = local.cmd('{0}'.format(minion), salt_cmd, myargs)

    # set vip in grain
    grain_cmd = 'grains.setval'
    mygrainargs = []
    mygrainargs.append('vip {0}'.format(newip))
    grain_ret = local.cmd('{0}'.format(minion), grain_cmd, mygrainargs)

    if len(cmd_ret[minion]) > 0:
        return "An error occurred in your request \n{0}".format(cmd_ret)
    else:
        return "The IP address has been assigned to the minion {0}".format(newip)
