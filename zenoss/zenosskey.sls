'Add zenoss key to root user':
  ssh_auth.present:
    - user: root
    - source: salt://ssh_keys/zenoss.id_rsa.pub
    - config: '%h/.ssh/authorized_keys'