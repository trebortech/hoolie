# State used to tag version of git code

include:
  - git

{% set refid = pillar.get('refid', '') %}

{% set tagid = refid[0,10] %}
{% set workingdir = "/tmp/" %}
{% set sshkey = "acme-site-demo" %}

####### STAGE KEYS #####################

"Set version grain":
  grains.present:
    - name: version
    - value: {{ refid }}

"Push ssh config file":
  file.managed:
    - name: /root/.ssh/config
    - source: salt://ssh/config
    - mode: 500
    - user: root
    - group: root
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
    - rev: {{ refid }}
    - identity: /root/.ssh/{{ sshkey }}.priv
    - force_clone: True
    - force_reset: True
    - update_head: True
    - require:
      - pkg: 'GIT software'

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

# Now tag version
"Tag version of ref":
  cmd.run:
    - name: 'git tag -a {{ tagid }} {{ refid }}'