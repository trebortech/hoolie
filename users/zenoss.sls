
# Create/Confirm Zenoss Admins group exists
'Zenoss Admins group available':
  group.present:
    - name: zenossadmins

# Move over the sudoer file for the Zenoss admin group
'Zenoss Admins sudoers file':
  file.managed:
    - name: '/etc/sudoers.d/10-zenossadmins'
    - source: salt://users/zenossadmins.sudoer
    - user: root
    - group: root
    - mode: 400

# Create the Zenoss user account
'Zenoss user available':
  user.present:
    - name: zenoss
    - fullname: Zenoss
    - shell: '/bin/bash'
    - password: '$1$xyz$K1m3vkKZXL1p36LriRJHK0'
    - groups:
      - zenossadmins
    - require:
      - group: 'Zenoss Admins group available'
  ssh_auth.present:
    - user: zenoss
    - source: salt://ssh_keys/zenoss.id_rsa.pub
    - config: '.ssh/authorized_keys'
    - require:
      - user: zenoss
