# -*- coding: utf-8 -*-
'''
An engine that reads Twilio text messages and puts them on eventbus

:configuration:

    Example configuration (master / minion config)
        engines:
            - twilio:
                account_sid: "<account side>"
                auth_token: "<auth token>"
                twilio_number: "+15555555555"
                interval: 10


:depends: twilio
'''

# Import Python libs
from __future__ import absolute_import
import logging
import time

# Import 3rd Party libs
try:
    from twilio.rest import TwilioRestClient
    HAS_TWILIO = True
except ImportError:
    HAS_TWILIO = False

# Import salt libs
import salt.utils
import salt.utils.event

log = logging.getLogger(__name__)


def __virtual__():
    if HAS_TWILIO:
        return True
    else:
        return False


def start(account_sid,
          auth_token,
          twilio_number,
          interval=10,
          tag='salt/engines/twilio'):

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

    #if not all(account_sid, auth_token, twilio_number):
    #    log.debug('Twilio account configuration not found')
    #    return

    client = TwilioRestClient(account_sid, auth_token)

    if client:
        messages = client.messages.list(to=twilio_number)
        log.trace('Num messages: {0}'.format(len(messages)))
        if len(messages) < 1:
            log.trace('Twilio engine has no texts')
            return

        for message in messages:
            item = {}
            item['id'] = str(message.sid)
            item['body'] = str(message.body)
            item['from'] = str(message.from_)
            item['sent'] = str(message.date_sent)
            item['images'] = []

            if int(message.num_media):
                media = client.media(message.sid).list()
                if len(media):
                    for pic in media:
                        item['images'].append(str(pic.uri))
            fire('{0}/{1}'.format(tag, item['from']), item)
            message.delete()

    time.sleep(interval)
