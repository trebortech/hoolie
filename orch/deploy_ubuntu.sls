
{% set instance = pillar.get('name', 'noname') %}
{% set deviceclass = pillar.get('deviceclass', '/Server/Linux') %}
{% set roles = pillar.get('role', 'norole') %}

"Deploy Instance":
  salt.runner:
    - name: cloud.profile
    - prof: demo-ubuntu
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

"Execute Highstate on new box":
  salt.state:
    - tgt: '{{ instance }}'
    - tgt_type: list
    - highstate: True

"Add to Zenoss":
  salt.runner:
    - name: zenoss.add_device
    - deviceName: {{ instance }}
    - deviceClass: {{ deviceclass }}
    - comments: "Are you worth your salt"