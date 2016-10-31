# Windows Orchestration

# Deploys Windows Servers
# Setups DNS, Firewall and hostname
# Add computers to domain

{% set profile = pillar.get('profile', 'demo-iis') %}
{% set instance = pillar.get('instance', 'demo1') %}
{% set domain = pillar.get('domain', 'saltstack.lab') %}
{% set size = pillar.get('size', 'small') %}
{% set datacenter = pillar.get('datacenter', 'Round Rock') %}
{% set resourcepool = pillar.get('resourcepool', 'DemoPool') %}


"Deploy New Windows Server":
  salt.runner:
    - name: fnni.deploy
    - profile: {{ profile }}
    - instances:
      - {{ instance }}
    - domain: {{ domain }}
    - datacenter: {{ datacenter }}
    - resourcepool: {{ resourcepool }}
    - size: {{ size }}

"Put short pause in for web system to catch up":
  salt.function:
    - tgt: 'saltmaster'
    - name: test.sleep
    - kwarg:
        length: 60

"Deploy initial setup states":
  salt.state:
    - tgt: {{ instance }}
    - tgt_type: list
    - sls:
      - sync
      - demo.network

wait_for_reboots:
  salt.wait_for_event:
    - name: salt/minion/*/start
    - id_list:
      - {{ instance }}


"Send Windows message to slack":
  salt.state:
    - tgt: 'saltmaster'
    - sls:
      - slack.blast
    - pillar:
        mymessage: "New Windows Servers have been deployed"

"Add Servers to AD":
  salt.state:
    - tgt: {{ instance }}
    - tgt_type: list
    - sls:
      - demo.addtodomain

"Wait for AD Reboot":
  salt.wait_for_event:
    - name: salt/minion/*/start
    - id_list:
      - {{ instance }}

"Put short pause in for system to catch up after AD boot":
  salt.function:
    - tgt: 'saltmaster'
    - name: test.sleep
    - kwarg:
        length: 30

"Execute Highstate on windows boxes":
  salt.state:
    - tgt: {{ instance }}
    - tgt_type: list
    - highstate: True

"Send windows server highstate message to slack":
  salt.state:
    - tgt: 'saltmaster'
    - sls:
      - slack.blast
    - pillar:
        mymessage: "Highstate for new servers has been executed"







