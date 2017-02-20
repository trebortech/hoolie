#!/usr/bin/env python

from __future__ import absolute_import
import logging

__virtualname__ = 'aws'

try:
    import requests
    HAS_REQUESTS = True  # pylint: disable=W0612
except ImportError:
    HAS_REQUESTS = False


def __virtual__():
    if HAS_REQUESTS:
        return __virtualname__
    else
        return False


def get_publicip():
    ret = {}
    result = requests.get("http://169.254.169.254/latest/meta-data/public-ipv4", proxies={'http': ''})
    ret['public_ip'] = str(result.text)
    return ret
