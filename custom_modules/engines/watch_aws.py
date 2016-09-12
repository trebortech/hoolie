# -*- coding: utf-8 -*-
'''
An engine that check AWS running instances and shuts down what is not needed


:configuration:

    Example configuration (master / minion config)
        engines:
            - watch_aws:
                keyid: xxxxxxxxxxx
                key: xxxxxxxxxxxxxxxxxxxxxx
                interval: 10
                runconfig:
                    - sse-demo: mo-fr  # mon-fri 24 hours
                    - orch-demo: mo-fr/8-17 # mon-fri 8am to 5pm
                    - default: mo-fr/8-17


:depends: boto
'''

# Import Python libs
from __future__ import absolute_import
import logging
import datetime
import time

# Import 3rd Party libs
try:
    from boto.ec2.connection import EC2Connection as ec2
    HAS_BOTO = True
except ImportError:
    HAS_BOTO = False

# Import salt libs
import salt.utils
import salt.utils.event

log = logging.getLogger(__name__)


def __virtual__():
    if HAS_BOTO:
        return True
    else:
        return False


def start(interval=10,
          runconfig=None,
          keyid=None,
          key=None,
          tag='salt/engines/watch_aws'):

    daysofweek = {
        0: 'mo',
        1: 'tu',
        2: 'we',
        3: 'th',
        4: 'fr',
        5: 'sa',
        6: 'su'
    }

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

    ec2conn = ec2(keyid, key)

    filters = {}
    filters['instance-state-name'] = 'running'

    runningInstances = ec2conn.get_all_instances(filters=filters)

    instanceList = []
    instanceName = []

    for reservation in runningInstances:
        try:
            environment = reservation.instances[0].tags['Environment'].lower()

            if environment != 'production':
                runtime = runconfig[environment].split('/')

                if len(runtime) == 1:
                    runninghours = 24
                else:
                    runninghours = runtime[1]

                today = datetime.datetime.today()
                weekday = today.weekday()
                hour = today.hour

                # Check if running during off hours
                if runninghours != 24:
                    start, finish = runninghours.split('-')
                    if hour < int(start) or hour >= int(finish):
                        instanceList.append(reservation.instances[0].id)
                        instanceName.append(reservation.instances[0].tags['Name'])

                # Check if running during off day
                if daysofweek[weekday] not in runtime[0]:
                    instanceList.append(reservation.instances[0].id)
                    instanceName.append(reservation.instances[0].tags['Name'])
        except:
            pass

    if len(instanceList) > 0:
        ec2conn.stop_instances(instanceList)
        msg = 'Engine is shutting down the following AWS instances {0}'.format(','.join(instanceName))
        fire('{0}'.format(tag), msg)
        
    time.sleep(interval)
