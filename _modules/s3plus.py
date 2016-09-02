from __future__ import absolute_import

import logging

# Import Salt libs

try:
    from boto.s3.connection import S3Connection as s3
    HAS_BOTO = True
except ImportError:
    HAS_BOTO = False

log = logging.getLogger(__name__)

__virtualname__ = 's3plus'


def __virtual__():
    if not HAS_BOTO:
        return False
    return __virtualname__


def get_file(objectid, bucketname, path):

    config = __pillar__.get('aws', None)
    key = config.get('key')
    keyid = config.get('keyid')

    s3conn = s3(keyid, key)

    bucket = s3conn.get_bucket(bucketname)
    objectkey = bucket.get_key(objectid)
    if objectkey:
        objectkey.get_contents_to_filename(path)

    return
