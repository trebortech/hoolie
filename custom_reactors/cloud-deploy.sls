#!py


def run():

    func = data['fun']
    event_ret = data['return']

    if event_ret and func == 'runner.cloud.profile':

        mymessage = []

        for minionname, value in data['return'].iteritems():

            minionip = data['return'][minionname]['privateIpAddress']

            mymessage.append('Cloud instance {0} has been deployed with IP address {1}'.format(
                minionname, minionip))

        mymessage = ' ------ '.join(mymessage)

        config = {}

        config['Notify cloud done'] = {
            'local.state.sls': [
                {'tgt': 'saltmaster'},
                {'arg': {
                    'slack.blast',
                    },
                },
                {'kwarg': {
                    'pillar': {'mymessage': mymessage},
                    },
                },
            ],
        }

        return config
    else:
        return {}
