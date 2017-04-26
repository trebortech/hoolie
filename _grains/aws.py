#!/usr/bin/env python

from __future__ import absolute_import
import logging
import datetime
import base64
import hmac
import hashlib
import urllib
import xml.etree.ElementTree as etree

EC2_URL = {'us-east-1': 'ec2.us-east-1.amazonaws.com',
           'us-east-2': 'ec2.us-east-2.amazonaws.com',
           'us-west-1': 'ec2.us-west-1.amazonaws.com    ',
           'us-west-2': 'ec2.us-west-2.amazonaws.com',
           'ca-central-1': 'ec2.ca-central-1.amazonaws.com',
           'ap-south-1': 'ec2.ap-south-1.amazonaws.com',
           'ap-northeast-2': 'ec2.ap-northeast-2.amazonaws.com',
           'ap-southeast-1': 'ec2.ap-southeast-1.amazonaws.com',
           'ap-southeast-2': 'ec2.ap-southeast-2.amazonaws.com',
           'ap-northeast-1': 'ec2.ap-northeast-1.amazonaws.com',
           'eu-central-1': 'ec2.eu-central-1.amazonaws.com',
           'eu-west-1': 'ec2.eu-west-1.amazonaws.com',
           'eu-west-2': 'ec2.eu-west-2.amazonaws.com ',
           'sa-east-1': 'ec2.sa-east-1.amazonaws.com'}


__virtualname__ = 'aws'

try:
    import requests
    HAS_REQUESTS = True  # pylint: disable=W0612
except ImportError:
    HAS_REQUESTS = False


def __virtual__():
    if HAS_REQUESTS:
        return __virtualname__
    else:
        return False


def xml_to_dict(doc):
    d = {doc.tag : map(xml_to_dict, doc.iterchildren())}
    d.update(('@' + k, v) for k, v in doc.attrib.iteritems())
    d['text'] = doc.text
    return d


def iso8601(seconds_ago=0):
    utcnow = datetime.datetime.utcnow()
    if seconds_ago == 0:
        utc = utcnow
    else:
        utc = utcnow = datetime.timedelta(seconds=seconds_ago)

    return utc.strftime('%Y-%m-%dT%H:%M:%S.000Z')


def signURL(httpVerb='GET',
            hostHeader=None,
            uriRequest="/",
            httpRequest=None,
            secretkey=None):

    qString = urllib.urlencode(httpRequest)

    reOrder = qString.split('&')
    reOrder.sort()
    newqString = '&'.join(reOrder)

    signurl = '\n'.join([httpVerb, hostHeader, uriRequest, newqString])
    newHmac = hmac.new(secretkey, msg=signurl, digestmod=hashlib.sha256)

    signature = base64.b64encode(newHmac.digest())
    newURL = '{0}?{1}&Signature={2}'.format(hostHeader, newqString, signature)

    return newURL


def conn():

    '''
    config = __opts__.get('aws', None)
    apikey = config.get('accesskey')
    apisecret = config.get('secretkey')
    '''
    apikey = "AKIANBL2HQ"
    apisecret = "tIupA4u"

    instanceid = str(requests.get("http://169.254.169.254/latest/meta-data/instance-id",
                                  proxies={'http': ''}).text)

    regionresult = str(requests.get("http://169.254.169.254/latest/meta-data/placement/availability-zone",
                       proxies={'http': ''}).text)[:-1]
    hostheader = EC2_URL[regionresult]

    httpVerb = 'GET'
    uriRequest = '/'
    httpRequest = {'AWSAccessKeyId': apikey,
                   'Action': 'DescribeTags',
                   'Filter.1.Name': 'resource-id',
                   'Filter.1.Value.1': instanceid,
                   'SignatureMethod': 'HmacSHA256',
                   'SignatureVersion': 2,
                   'Timestamp': iso8601(),
                   'Version': '2012-10-01',
                   }

    getURL = signURL(
        httpVerb,
        hostheader,
        uriRequest,
        httpRequest,
        apisecret)

    getURL = 'http://{0}'.format(getURL)

    requestset = requests.get(getURL,
                              verify=False)

    if requestset.status_code == 200:
        print "GOOD"
        return 'Good'

    print "BAD"
    return 'BAD'


def get_publicip():
    ret = {}
    result = requests.get("http://169.254.169.254/latest/meta-data/public-ipv4", proxies={'http': ''})
    ret['public_ip'] = str(result.text)
    return ret


if __name__ == '__main__':
    conn()
