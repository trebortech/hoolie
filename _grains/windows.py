#!/usr/bin/env python

from __future__ import absolute_import
import json
import logging

import salt.utils

import salt.modules.cmdmod

__salt__ = {
    'cmd.run': salt.modules.cmdmod._run_quiet
}

__virtualname__ = 'windows'


def __virtual__():
    if salt.utils.is_windows():
        return __virtualname__
    else:
        return False


def _srvmgr(func, as_json=False):

    if as_json:
        command = 'ConvertTo-Json -Compress -Depth 4 -InputObject @({0})'.format(func)
    else:
        command = func

    return __salt__['cmd.run'](
        command,
        shell='powershell',
        python_shell=True)


def get_ad():
    ret = {}
    pscmd = []
    pscmd.append(r'Import-Module activedirectory;')
    command = ''.join(pscmd)

    if len(_srvmgr(command)) > 0:
        ret['activedirectory'] = False
    else:
        ret['activedirectory'] = True

    return ret


def get_dotnet():
    ret = {}
    pscmd = []
    pscmd.append(r"Get-ChildItem 'HKLM:\SOFTWARE\Microsoft\NET Framework Setup\NDP' -recurse |")
    pscmd.append(r"Get-ItemProperty -name Version,Release -EA 0 |")
    pscmd.append(r"Where { $_.PSChildName -match '^(?!S)\p{L}'} |")
    pscmd.append(r"Select PSChildName, Version, Release")

    command = ''.join(pscmd)

    items = json.loads(_srvmgr(command, as_json=True), strict=False)

    ret['dotnet'] = items
    return ret


def get_lastbootup():
    ret = {}
    pscmd = []
    pscmd.append(r"$os = get-wmiobject win32_operatingsystem;")
    pscmd.append(r"$os.ConvertToDateTime($os.lastbootuptime).ToString()")

    command = ''.join(pscmd)

    items = json.loads(_srvmgr(command, as_json=True), strict=False)

    ret['lastbootup'] = items
    return ret


