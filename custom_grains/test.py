# -*- coding: utf-8 -*-

from __future__ import absolute_import

# Import python libs
import os

# Import third party libs
import yaml
import logging

# Import salt libs
import salt.utils

log = logging.getLogger(__name__)


def adtest():
    '''
    Return the default shell to use on this system
    '''
    # Provides:
    #   shell
    return {'ad': 'False'}