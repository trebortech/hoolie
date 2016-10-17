
# IIS Orchestration

# Deploys IIS Servers
# Setups DNS, Firewall and hostname
# Add computers to domain

# Deploy 2 new IIS instances

{% set name = pillar.get('name', 'iis') %}


"Deploy IIS New Server":
  salt.runner:
    - name: cloud.profile
    - prof: arm-windows
    - instances:
      - {{ name }}
    - vm_overrides:
      - minion:
        - grains:
          - roles: iis

"Put short pause in for web system to catch up":
  salt.function:
    - tgt: 'master1'
    - name: test.sleep
    - kwarg:
        length: 60

"Deploy initial setup states":
  salt.state:
    - tgt: {{ name }}
    - tgt_type: list
    - sls:
      - sync
      - demo.network

wait_for_reboots:
  salt.wait_for_event:
    - name: salt/minion/*/start
    - id_list:
      - {{ name }}

"Send IIS message to slack":
  salt.state:
    - tgt: 'master1'
    - sls:
      - slack.blast
    - pillar:
        mymessage: "New IIS Servers have been deployed"

"Add Servers to AD":
  salt.state:
    - tgt: {{ name }}
    - tgt_type: list
    - sls:
      - demo.addtodomain

"Wait for AD Reboot":
  salt.wait_for_event:
    - name: salt/minion/*/start
    - id_list:
      - {{ name }}

"Put short pause in for web system to catch up after AD boot":
  salt.function:
    - tgt: 'master1'
    - name: test.sleep
    - kwarg:
        length: 30

"Execute Highstate on web boxes":
  salt.state:
    - tgt: {{ name }}
    - tgt_type: list
    - highstate: True

"Send web server highstate message to slack":
  salt.state:
    - tgt: 'saltmaster'
    - sls:
      - slack.blast
    - pillar:
        mymessage: "Highstate for new web servers has been executed"







