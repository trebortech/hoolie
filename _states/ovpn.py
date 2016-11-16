'''
Create ovpn CA and client certs

'''

# Import salt libs
import logging
import os

__virtualname__ = 'ovpn'

def __virtual__():
    return __virtualname__


def _user_config_dir(username, name, workingpath):

    userdir = '{0}/{1}/{2}'.format(workingpath, name, username)

    if not os.path.exists(userdir):
        os.makedirs(userdir)

    return userdir


def ca(name, days=365, C='US', ST='Texas', L='Round Rock', O='SaaS',
       emailAddress='noreply@acme.com', cacert_path='/etc/pki'):

    # name = homevpn
    # will become
    # homevpn_ca_cert

    ret = {'name': name,
           'changes': {},
           'result': None,
           'comment': ''}

    change = {}
    # Check to see if CA exists
    if __salt__['tls.ca_exists'](name, cacert_path):
        ret['changes'] = {'results': 'CA Already exists'}
        ret['comment'] = '{0} already exists'.format(name)
        ret['result'] = True
    else:
        # Create CA
        __salt__['tls.create_ca'](name,
                                  days=days,
                                  CN=name,
                                  C=C,
                                  ST=ST,
                                  L=L,
                                  O=O,
                                  emailAddress=emailAddress,
                                  cacert_path=cacert_path)
        ret['changes'] = {'results': 'CA Created'}
        ret['result'] = True
        ret['comment'] = 'Created new CA for {0}'.format(name)

    return ret

def user(name, CN, workingpath):

    ret = {'name': name,
           'changes': {},
           'result': None,
           'comment': ''}

    changes = []

    if type(CN) is list:
        for user in CN:
            crtpath = _user_config_dir(user, name, workingpath)
            csr = __salt__['tls.create_csr'](name, csr_path=crtpath, CN=user)
            crt = __salt__['tls.create_ca_signed_cert'](name, cert_path=crtpath, CN=user)
            
            if 'already exists' in crt:
                changes.append('user {0} certificate already exists'.format(user))           
            else:
                changes.append('user {0} cretificate created'.format(user)) 

    else:
        crtpath = _user_config_dir(user, name, workingpath)
        csr = __salt__['tls.create_csr'](name, csr_path=crtpath, CN=CN)
        crt = __salt__['tls.create_ca_signed_cert'](name, cert_path=crtpath, CN=CN)
        if 'already exists' in crt:
            changes.append('user {0} certificate already exists'.format(user))           
        else:
            changes.append('user {0} cretificate created'.format(user)) 

        changes.append('user {0} created'.format(CN))


    ret['changes'] = {'results': changes}
    ret['result'] = True
    ret['comment'] = 'Certs have been created'
    return ret