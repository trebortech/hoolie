'''
An engine to pull lines from Google Sheets into salt stack events

:configuration:

    Example configuration (master config)
        engines:
            - gspread:
                documentids:
                    - 1mLwgEE8asxCWReklhePJYSEqfW8mYLogjJzVImsZE8Y
                    - 1P7XCvx2jm6U2OMX5r2Zk-SAtxq2LnGmgr4GBt3VIV-w
                interval: 10
                keyfilelocation: /srv/client.json

:depends:
    gspread
    oauth2client

'''


from __future__ import absolute_import
import logging
import time

log = logging.getLogger(__name__)


try:
    import gspread
    from gspread.exceptions import WorksheetNotFound
    from oauth2client.service_account import ServiceAccountCredentials
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False

def __virtual__():
    if HAS_LIBS:
        return True
    else:
        return False

# Import salt libs
import salt.utils
import salt.utils.event

def start(documentids,
          keyfilelocation,
          interval=10,
          tag='salt/engines/gspread',
          adminsheet='saltengine'):

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

    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(keyfilelocation, scope)
    gc = gspread.authorize(credentials)

    for docid in documentids:
        
        # Open the spreadsheet by the id
        odoc = gc.open_by_key(docid)

        # Get the first worksheet
        wks = odoc.get_worksheet(0)

        # Get the first line as the values for keys
        titlerow = filter(None, wks.row_values(1))

        # Get worksheet that engine data to find what row last processed
        try:
            dbdoc = odoc.worksheet(adminsheet)
            lastrow = dbdoc.acell('A1').value
        except WorksheetNotFound:
            dbdoc = odoc.add_worksheet(adminsheet, 1, 1)
            dbdoc.update_acell('A1', '1')
            lastrow = '1'

        nextlineid = int(lastrow) + 1
        lineloop = True
        while lineloop:
            nextline = filter(None, wks.row_values(nextlineid))
            evtdata = {'doctitle': odoc.title,
                       'docid': odoc.id,
                       'data': {}}
            outdata = {}
            if nextline:
                outdata = dict(zip(titlerow, nextline))
                evtdata['data'] = outdata
                # Send event
                fire('{0}/{1}'.format(tag, docid), evtdata)
                nextlineid = nextlineid + 1
            else:
                # Update dbsheet
                nextlineid = nextlineid - 1
                dbdoc.update_acell('A1', str(nextlineid))
                lineloop = False

    time.sleep(interval)
