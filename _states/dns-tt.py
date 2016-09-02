'''
DNS Management

'''

# Import python libs
import logging
import re

# Import salt libs
import salt.utils

log = logging.getLogger(__name__)


# Define the module's virtual name
__virtualname__ = 'dns-tt'

try:
    from boto.route53 import Route53Connection as route53
    HAS_BOTO = True
except ImportError:
    HAS_BOTO = False

__virtualname__ = 'aws_route53'

def __virtual__():
    if not HAS_BOTO:
        return False
    return __virtualname__


def create_dns_record(url, siteip, key, token, recordtype='A', ttl=300):
    
    __salt__['aws_route53.create_dns_record'](
        recordtype,
        url,
        siteip,
        ttl,
        key,
        token)
