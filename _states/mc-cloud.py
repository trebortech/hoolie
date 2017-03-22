# -*- coding: utf-8 -*-
'''
State Module to run MC Cloud docker commands
'''

from __future__ import absolute_import

__virtualname__ = 'mc-cloud'


def __virtual__():
    return __virtualname__


def cliqrbuild(name, cliqrtagversion, cliqrtarget, cliqrsourceimage='cliqr/worker'):

    ret = {'name': name,
           'changes': {},
           'result': None,
           'comment': ''}

    # Set values
    cliqrsource = '{0}:{1}'.format(cliqrsourceimage, 'latest')
    cliqrnew = '{0}:{1}'.format(cliqrsourceimage, cliqrtagversion)
    cliqrpath = '/root/cliqr_worker_{0}.tar'.format(cliqrtagversion)
    cliqrtargetpath = '{0}:{1}'.format(cliqrtarget, cliqrpath)

    # Tag cliqr latest

    __salt__['dockerng.tag'](name=cliqrsource,
                             image=cliqrnew)

    # Export to tar file

    __salt__['dockerng.export'](name=cliqrnew,
                                path=cliqrpath,
                                makedirs=True)

    # Copy tar to remote host
    __salt__['rsync.rsync'](src=cliqrpath,
                            dst=cliqrtargetpath)

    ret['result'] = 'Cliqr Build Complete'
    ret['changes'] = {'results': 'New tag version created: {0}'.format(cliqrnew)}
    ret['comment'] = 'Image has been created and transferred'

    return ret
