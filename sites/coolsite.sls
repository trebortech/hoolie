# Cool site pulls from
# https://github.com/trebortech/ACME.git

include:
  - nginx
  - git

{% set workingdir = "/usr/share/nginx/html/" %}
{% set sshkey = "acme-site-demo" %}


{% if pillar['version'] is defined %}
{% set env = pillar['version'] %}
{% else %}
{% set env = grains.get('version', 'dev') %}
{% endif %}


####### STAGE KEYS #####################

"Set version grain":
  grains.present:
    - name: version
    - value: {{ env }}

"Set version grain":
  grains.present:
    - name: role
    - value: 'coolsite'

"Push ssh config file":
  file.managed:
    - name: /root/.ssh/config
    - source: salt://ssh/config
    - mode: 500
    - user: root
    - group: root
    - makedirs: True
    - template: jinja
    - defaults:
        SSHKEY: {{ sshkey }}

"Push ssh keys for github":
  file.managed:
    - name: /root/.ssh/{{ sshkey }}.priv
    - source: salt://files/{{ sshkey }}.priv
    - makedirs: True
    - mode: 600
    - user: root
    - group: root
    - require:
      - file: "Push ssh config file"

####### PULL IN ACME DEV CODE ##########

"Pull in ACME site code":
  git.latest:
    - name: git@github.com:trebortech/ACME.git
    - target: {{ workingdir }}
    - rev: {{ env }}
    - identity: /root/.ssh/{{ sshkey }}.priv
    - force_clone: True
    - force_reset: True
    - force_fetch: True
    - update_head: True
    - require:
      - pkg: 'GIT software'
      - pkg: 'Deploy NGINX package'

####### UPDATE GIT CONFIG  #############
"Setup {{ env }} email config":
  git.config_set:
    - name: user.email
    - value: rbooth@saltstack.com
    - repo: {{ workingdir }}
    - require:
      - git: "Pull in ACME site code"

"Setup {{ env }} name config":
  git.config_set:
    - name: user.name
    - value: trebortech
    - repo: {{ workingdir }}
    - require:
      - git: "Pull in ACME site code"

"Setup core editor":
  git.config_set:
    - name: core.editor
    - value: vim
    - repo: {{ workingdir }}
    - require:
      - git: "Pull in ACME site code"

"Confirm NGINX service started after git deploy":
  service.running:
    - name: nginx
    - watch:
      - git: "Pull in ACME site code"

