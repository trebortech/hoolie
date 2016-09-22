# -*- coding: utf-8 -*-
'''
An engine that check AWS running instances and shuts down what is not needed


:configuration:

    Example configuration (master / minion config)
        engines:
            - resource_manager:
                keygrain: minionenv
                interval: 10
                runconfig:
                    - sse-demo: mo,tu,we,th,fr  # mon-fri 24 hours
                    - orch-demo: mo,fr/8-17 # mon and fri 8am to 5pm
                    - default: mo,tu,we,th,fr/8-17


'''

# Import Python libs
from __future__ import absolute_import
import logging
import datetime
import time

# Import salt libs
import salt.utils
import salt.utils.event

log = logging.getLogger(__name__)



def _get_minions(tgt):

    minions = []

    tgt = tgt
    expr_form = 'grain'

    pillar_util = salt.utils.master.MasterPillarUtil(
        tgt,
        expr_form,
        use_cached_grains=True,
        grains_fallback=False,
        opts=__opts__)

    cached_grains = pillar_util.get_minion_grains()

    for item in cached_grains.viewitems():
        if len(item[1]) > 0:
            minions.append(item[0])

    return minions


def _check_if_running(minions):
    cleanlist = []

    ret = salt.runners.manage.up(tgt=minions, expr_form='list')

    log.debug('****** RETURN DATA {0}'.format(ret))
    #for minion in minions:
    #    if __salt__['test.ping'](minion):
    #        cleanlist.append(minion)
    #return cleanlist
    return

def _stop_minions(minions):
    __salt__['system.shutdown'](minions)


def _start_minions(minions):



def start(interval=10,
          runconfig=None,
          keygrain=None
          tag='salt/engines/cloud_jobs'):


    if __opts__.get('__role') == 'master':
        fire_master = salt.utils.event.get_master_event(
            __opts__,
            __opts__['sock_dir']).fire_event
    else:
        fire_master = None

    def fire(tag, msg):
        if fire_master:
            fire_master(msg, tag)
        else:
            __salt__['event.send'](tag, msg)

    today = datetime.datetime.today()
    weekday = today.weekday()
    hour = today.hour

    for grain in runconfig:
        runtime = runconfig[grain].split('/')
        
        if len(runtime) == 1:
            runninghours = 24
        else:
            runninghours = runtime[1]

        if runninghours != 24:
            start, finish = runninghours.split('-')
            if hour < int(start) or hour >= int(finish):
                instanceList = _get_minions(grain)
            elif daysofweek[weekday] not in runtime[0]:
                instanceList = _get_minions(grain)
        else:
            if daysofweek[weekday] not in runtime[0]:
                instanceList = _get_minions(grain)

        # instanceList now has a list of minions that should be shutdown
        # check to see if they are running
        cleanlist = _check_if_running(instanceList)

        if len(cleanlist) > 0:
            _stop_minions(cleanlist)


    if len(instanceList) > 0:
        ec2conn.stop_instances(instanceList)
        msg = 'Engine is shutting down the following AWS instances {0}'.format(','.join(instanceName))
        fire('{0}'.format(tag), msg)
        
    time.sleep(interval)
