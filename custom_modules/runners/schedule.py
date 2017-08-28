from __future__ import absolute_import
import logging
import os
import yaml

import salt.utils.event
import salt.syspaths

import salt.ext.six as six

log = logging.getLogger(__name__)


def __virtual__():
    return True


def _persist(schedule, opts=None):
    if opts is None:
        opts = __opts__

    config_dir = opts.get('conf_dir', None)
    if config_dir is None and 'conf_file' in opts:
        config_dir = os.path.dirname(opts['conf_file'])
    if config_dir is None:
        config_dir = salt.syspaths.CONFIG_DIR

    schedule_conf = os.path.join(config_dir, 'master.d/_schedule.conf')

    try:
        with salt.utils.fopen(schedule_conf, 'wb+') as fp_:
            fp_.write(
                salt.utils.to_bytes(
                    yaml.dump({'schedule': schedule})
                )
            )
    except (IOError, OSError):
        log.error('Failed to persist the updated schedule',
                  exc_info_on_loglevel=logging.DEBUG)
    return True


def add_job(data, persist=True, opts=None):
    if opts is None:
        opts = __opts__

    if not isinstance(data, dict):
        raise ValueError('Scheduled jobs have to be of type dict.')
    if not len(data) == 1:
        raise ValueError('You can only schedule one new job at a time.')

    # if enabled is not included in the job,
    # assume job is enabled.
    for job in data.keys():
        if 'enabled' not in data[job]:
            data[job]['enabled'] = True

    new_job = next(six.iterkeys(data))

    schedule = opts['schedule']

    if new_job in schedule:
        log.info('Updating job settings for scheduled '
                 'job: {0}'.format(new_job))
    else:
        log.info('Added new job {0} to scheduler'.format(new_job))

    schedule.update(data)

    _persist(schedule)


def list(opts=None):
    '''
    List the current schedule items
    '''
    if opts is None:
        opts = __opts__
    schedule = {}
    if 'schedule' in opts:
        schedule.update(opts['schedule'])

    # Fire the complete event back along with the list of schedule
    fire_master = salt.utils.event.get_master_event(
            opts,
            opts['sock_dir']).fire_event

    msg = {'complete': True, 'schedule': schedule}
    tag = '/salt/master/master_schedule_list_complete'

    fire_master(msg, tag)

    return True
