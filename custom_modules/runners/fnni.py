'''
FNNI custom runner to manage cloud deployments
'''
from __future__ import absolute_import

import os
import sys

import salt.utils.sdb as sdb
import infoblox as ib
import salt.cloud

import logging

sys.path.insert(0, os.path.abspath('.'))

log = logging.getLogger(__name__)


def __virtual__():
    return True


def _get_client():
    client = salt.cloud.CloudClient(
        os.path.join(os.path.dirname(__opts__['conf_file']), 'cloud')
    )
    return client


def deploy(profile, type='iis', numinstances=1, domain=None, size='small', opts=None, **kwargs):

    if opts is None:
        opts = __opts__

    for instance in instances:
        # Deploy cloud instance with IP address if provided

        vm_overrides = {}

        if size == 'small':
            vm_overrides['num_cpus'] = '1'
            vm_overrides['memory'] = '4GB'

        elif size == 'medium':
            vm_overrides['num_cpus'] = '1'
            vm_overrides['memory'] = '6GB'

        elif size == 'large':
            vm_overrides['num_cpus'] = '2'
            vm_overrides['memory'] = '8GB'

        client = _get_client()
        info = client.profile(profile=profile, names=[instance], vm_overrides=vm_overrides, **kwargs)

        for ip in info[instance]['private_ips']:
            if len(ip) < 16:
                ipassigned = ip

        # Setup the DNS inside of the Infoblox system
        dnsset = ib.set_host(instance, domain, ipassigned, opts)

        if dnsset:
            return True
        else:
            return False

    return False
