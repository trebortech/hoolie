#!py
import time
def run():

    if 'Alerted on' in data['data']:
        func = data['data']['Alerted on']
        minionid = data['data']['id']
        tag = data['tag'].replace('\\', '\\\\')

        mymessage = 'A {0} event was noticed on minion {1} for tag {2}'.format(
        func, minionid, tag)

        config = {}

        # Send slack message
        
        config['Notify user of event'] = {
            'local.state.sls': [
                {'tgt': 'saltmaster'},
                {'arg': {
                    'slack.blast',
                    },
                },
                {'kwarg': {
                    'pillar': {'mymessage': mymessage },
                    },
                },
            ],
        }


        # Execute state on minion
        config['Execute state to revert file change'] = {
            'local.state.sls': [
                {'tgt': minionid},
                {'arg': {
                    'demo.testconfigs',
                    },
                },
            ],
        }
        time.sleep(3)
        return config
    elif 'No File' in data['data']:
        filename = data['data']['No File'].replace('\\', '\\\\')
        minionid = data['data']['id']

        mymessage = 'File {0} does not exists on minion {1}'.format(filename, minionid)

        config = {}

        config['Notify user of event'] = {
            'local.state.sls': [
                {'tgt': 'saltmaster'},
                {'arg': {
                    'slack.blast',
                    },
                },
                {'kwarg': {
                    'pillar': {'mymessage': mymessage },
                    },
                },
            ],
        }
        time.sleep(3)
        return {} #config
    else:
        return {}

