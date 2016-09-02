#!py

def run():
    func = data['fun']
    event_ret = data['return']

    if event_ret and func == 'runner.cloud.profile':
        mymessage = []
        for minionname, value in data['return'].iteritems():
            # AWS will return privateIpAddress
            if 'privateIpAddress' in data['return'][minionname]:
                minionip = data['return'][minionname]['privateIpAddress']
            
            # vSphere will return private_ips. List with ipv6 address
            if 'private_ips' in data['return'][minionname]:
                for ip in data['return'][minionname]['private_ips']:
                    if ":" not in ip:
                        minionip = ip
            
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