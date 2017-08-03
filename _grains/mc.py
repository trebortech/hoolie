#!/usr/bin/env python

from __future__ import absolute_import

import os
import logging
import socket

import salt.utils

__virtualname__ = 'mayohostname'

'''
CC | T | XXX | 123 | F | NN | O

Grains available
- citycode
- hosttype
- hostfunc
- funcid
- functype
- clusternode

salt-call grains.item citycode

'''


def _get_funcid(funcid):
    try:
        funcid = int(funcid)
        if funcid >= 000 and funcid <= 399:
            retid = 'PROD'
        elif funcid >= 400 and funcid <= 499:
            retid = 'BUILD'
        elif funcid >= 500 and funcid <= 599:
            retid = 'MOCK'
        elif funcid >= 600 and funcid <= 699:
            retid = 'TRAIN'
        elif funcid >= 700 and funcid <= 799:
            retid = 'CERT'
        elif funcid >= 800 and funcid <= 899:
            retid = 'DEV'
        elif funcid >= 900 and funcid <= 999:
            retid = 'TEST'
    except:
        retid = 'FAIL'
    return retid


def __virtual__():
    return __virtualname__


def parse_hostname():
    ret = {}

    hostname = socket.gethostname().upper()

    ret['citycode'] = {
        'JA': 'Jacksonville',
        'RO': 'Rochester',
        'PX': 'Phoenix',
        'SC': 'Scottsdale',
        'CL': 'Cloud'}.get(hostname[:2], 'UNKNOWN')

    ret['hosttype'] = {
        'E': 'VMware VM - Windows',
        'F': 'VMware VM - Linux',
        'P': 'Physical - Windows',
        'Q': 'Physical - Linux',
        'C': 'Cluster Resource',
        'L': 'Linux VM Cluster Farm',
        'D': 'Virtual Desktop VM Farm',
        'W': 'Windows'}.get(hostname[2:3], 'UNKNOWN')

    ret['hostfunc'] = {
        'VCE': 'VCEM servers'}.get(hostname[3:6], 'UNKNOWN')

    ret['funcid'] = _get_funcid(hostname[6:9])

    ret['functype'] = {
        'A': 'Application Servers',
        'F': 'File Server',
        'M': 'Microsoft Cluster',
        'O': 'Oracle',
        'P': 'Print Server',
        'Q': 'SQL Servers'}.get(hostname[9:10], 'UNKNOWN')

    ret['clusternode'] = hostname[10:]

    return ret
