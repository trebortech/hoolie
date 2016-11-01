# Linux Orchestration

# Deploys Linux Servers

{% set profile = pillar.get('profile', 'demo-ubuntu') %}
{% set instance = pillar.get('instance', 'demo1') %}
{% set domain = pillar.get('domain', 'saltstack.lab') %}
{% set size = pillar.get('size', 'small') %}
{% set datacenter = pillar.get('datacenter', 'Round Rock') %}
{% set resourcepool = pillar.get('resourcepool', 'DemoPool') %}


"Deploy New Linux Server":
  salt.runner:
    - name: fnni.deploy
    - profile: {{ profile }}
    - instances:
      - {{ instance }}
    - domain: {{ domain }}
    - datacenter: {{ datacenter }}
    - resourcepool: {{ resourcepool }}
    - size: {{ size }}

"Put short pause in for linux system to catch up":
  salt.function:
    - tgt: 'saltmaster'
    - name: test.sleep
    - kwarg:
        length: 5

"Send Linux message to slack":
  salt.state:
    - tgt: 'saltmaster'
    - sls:
      - slack.blast
    - pillar:
        mymessage: "New Linux Servers have been deployed"

"Execute Highstate on Linux boxes":
  salt.state:
    - tgt: {{ instance }}
    - tgt_type: list
    - highstate: True

"Put short pause in for box system to catch up":
  salt.function:
    - tgt: 'saltmaster'
    - name: test.sleep
    - kwarg:
        length: 5

"Send Linux server highstate message to slack":
  salt.state:
    - tgt: 'saltmaster'
    - sls:
      - slack.blast
    - pillar:
        mymessage: "Highstate for new servers has been executed"







