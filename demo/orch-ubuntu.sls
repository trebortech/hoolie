# Linux Orchestration
# Deploy Linux Server in AWS

{% set profile = pillar.get('profile', '') %}
{% set instance = pillar.get('servername', '') %}
{% set role = pillar.get('role', '') %}


"Deploy New Linux Server":
  salt.runner:
    - name: cloud.profile
    - prof: {{ profile }}
    - instances:
      - {{ instance }}
    - vm_overrides:
      minion:
        grains:
          roles: {{ role }}

"Wait for minion service to start":
  salt.wait_for_event:
    - name: salt/minion/*/start
    - id_list:
      - {{ instance }}

"Deploy initial setup states":
  salt.state:
    - tgt: '{{ instance }}'
    - tgt_type: list
    - sls:
      - runonce.testfile

"Execute Highstate on new box":
  salt.state:
    - tgt: '{{ instance }}'
    - tgt_type: list
    - highstate: True
