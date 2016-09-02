

{% set workingdir = "/srv/poc" %}
{% set env = grains.get('branch', 'master') %}


# Init the poc instance


# Pull down the /srv/poc repo

"Pull in POC site code":
  git.latest:
    - name: git@srv-poc:trebortech/salt-poc.git
    - target: {{ workingdir }}
    - rev: {{ env }}
    - branch: {{ env }}
    - identity: /etc/salt/master.d/salt-poc-docker.priv
    - force_checkout: True
    - force_clone: True
