# -*- coding: utf-8 -*-
'''
State Module to run MC Cloud docker commands
'''

from __future__ import absolute_import
from salt.exceptions import CommandExecutionError

__virtualname__ = 'mc-cloud'


def __virtual__():
    return __virtualname__


def cliqrbuild(name,
               cliqrtagversion,
               buildtarget,
               targetdir='/root',
               cliqrsourceimage='cliqr/worker'):

    ret = {'name': name,
           'changes': {},
           'result': None,
           'comment': ''}

    ret['changes']['Errors'] = []
    ret['changes']['Results'] = []

    # Set values
    cliqrsource = '{0}:{1}'.format(cliqrsourceimage, 'latest')
    cliqrnew = '{0}:{1}'.format(cliqrsourceimage, cliqrtagversion)
    cliqrimagepath = '{0}/cliqr_worker_{1}.tar'.format(targetdir, cliqrtagversion)
    cliqrtargetpath = '{0}:{1}'.format(buildtarget, cliqrimagepath)

    # Tag cliqr latest

    __salt__['dockerng.tag'](name=cliqrsource,
                             image=cliqrnew)

    # Export to tar file

    __salt__['dockerng.save'](name=cliqrnew,
                              path=cliqrimagepath,
                              makedirs=True)

    # Copy tar to remote host
    __salt__['rsync.rsync'](src=cliqrimagepath,
                            dst=cliqrtargetpath)

    ret['result'] = 'Cliqr Build Complete'
    ret['changes']['Results'] = 'New tag version created: {0}'.format(cliqrnew)
    ret['comment'] = 'Image has been created and transferred'

    return ret


def mayobuild(name,
              cliqrtagversion,
              mayotagversion,
              mayorepo,
              dockerfilepath,
              sourcedir='/root',
              builddir='/root/mayobuild',
              cliqrsourceimage='cliqr/worker'):

    ret = {'name': name,
           'changes': {},
           'result': None,
           'comment': ''}

    ret['changes']['Errors'] = []
    ret['changes']['Results'] = []

    cliqrimagefile = 'cliqr_worker_{0}.tar'.format(cliqrtagversion)
    mayoimagefile = 'cliqr_worker_{0}.tar'.format(mayotagversion)

    cliqrimport = '{0}:{1}'.format(cliqrsourceimage, cliqrtagversion)
    cliqrstage = '{0}:latest'.format(cliqrsourceimage)
    mayostage = '{0}:{1}'.format(cliqrsourceimage, mayotagversion)

    # Clean up workspace
    __salt__['file.remove'](builddir)
    __salt__['file.mkdir'](builddir)

    # Remove existing images for Cliqr
    try:
        __salt__['dockerng.rmi']('{0}:{1}'.format(cliqrsourceimage, 'latest'))
        ret['changes']['Results'].append('{0}:latest has been removed'.format(cliqrsourceimage))
    except CommandExecutionError:
        ret['changes']['Errors'].append('{0}:latest did not exists'.format(cliqrsourceimage))

    # Load cliqr image from tar file
    __salt__['dockerng.load']('{0}/{1}'.format(sourcedir, cliqrimagefile), cliqrstage)
    ret['changes']['Results'].append('{0} has been loaded into docker images'.format(cliqrimagefile))

    # Pull down Mayo-Cliqr docker file
    __salt__['git.clone'](cwd=builddir, url=mayorepo)
    ret['changes']['Results'].append('Repo was cloned')

    # Build new image with docker file
    __salt__['dockerng.build'](path='{0}/{1}'.format(builddir, dockerfilepath),
                               image=mayostage,
                               cache=False)

    # Export Mayo-Cliqr docker image
    try:
        __salt__['dockerng.save'](name=mayostage,
                                  path='{0}/{1}'.format(sourcedir, mayoimagefile),
                                  makedirs=True)
        ret['changes']['Results'].append('New Mayo Tag version created: {0}'.format(mayostage))
    except CommandExecutionError:
        ret['changes']['Errors'].append('{0} already exists'.format(mayostage))

    # Create md5 has file of tar file
    filehash = __salt__['hashutil.md5_digest']('{0}/{1}'.format(sourcedir, mayoimagefile))
    __salt__['file.write']('{0}/{1}.md5'.format(sourcedir, mayoimagefile), filehash)
    ret['changes']['Results'].append('New file hash created {0}/{1}.md5'.format(sourcedir, mayoimagefile))

    ret['result'] = 'Mayo Docker Build Complete'
    ret['comment'] = 'All complete'

    return ret


def deploymayobuild(name,
                    mayotagversion,
                    buildserver,
                    sourcedir,
                    cliqrsourceimage='cliqr/worker'):

    ret = {'name': name,
           'changes': {},
           'result': None,
           'comment': ''}

    ret['changes']['Errors'] = []
    ret['changes']['Results'] = []

    mayoimagepath = '{0}/cliqr_worker_{1}.tar'.format(sourcedir, mayotagversion)
    mayosourcepath = '{0}:{1}'.format(buildserver, mayoimagepath)

    # Copy from build server
    __salt__['rsync.rsync'](src=mayosourcepath,
                            dst=mayoimagepath)

    # Load new tar file
    __salt__['dockerng.load'](mayoimagepath, '{0}:latest'.format(cliqrsourceimage))

    # Remove the tar file
    __salt__['file.remove'](mayoimagepath)

    ret['result'] = 'Mayo Docker Deploy Complete'
    ret['comment'] = 'All complete'

    return ret
