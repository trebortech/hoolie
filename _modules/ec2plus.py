

from __future__ import absolute_import
import logging
from distutils.version import LooseVersion as _LooseVersion

# Import Salt libs
import salt.utils
import salt.utils.compat

try:
    # pylint: disable=unused-import
    import boto
    import boto.ec2
    # pylint: enable=unused-import
    HAS_BOTO = True
except ImportError:
    HAS_BOTO = False


log = logging.getLogger(__name__)


def __virtual__():
    '''
    Only load if boto libraries exist and if boto libraries are greater than
    a given version.
    '''
    required_boto_version = '2.8.0'
    # the boto_ec2 execution module relies on the connect_to_region() method
    # which was added in boto 2.8.0
    # https://github.com/boto/boto/commit/33ac26b416fbb48a60602542b4ce15dcc7029f12
    if not HAS_BOTO:
        return (False, "The boto_ec2 module cannot be loaded: boto library not found")
    elif _LooseVersion(boto.__version__) < _LooseVersion(required_boto_version):
        return (False, "The boto_ec2 module cannot be loaded: boto library version incorrect ")
    else:
        __utils__['boto.assign_funcs'](__name__, 'ec2', pack=__salt__)
        return True


def __init__(opts):
    salt.utils.compat.pack_dunder(__name__)
    if HAS_BOTO:
        __utils__['boto.assign_funcs'](__name__, 'ec2')


def assign_private_ip(
    interface_id,
    secondary_count=1,
    key=None,
    keyid=None,
    region=None,
    profile=None):

    conn = _get_conn(region=region, key=key, keyid=keyid, profile=profile)

    try:
        return conn.assign_private_ip_addresses(
            network_interface_id=interface_id,
            secondary_private_ip_address_count=secondary_count)
    except boto.exception.BotoServerError as e:
        log.error(e)
        return []
  

