
{% set instance = pillar.get('name', 'noname') %}
{% set deviceclass = pillar.get('deviceclass', '/Server/Linux') %}
{% set zCommandUsername = pillar.get('zCommandUsername', 'ubunut') %}
{% set role = pillar.get('role', 'norole') %}


"Deploy Instance":
  salt.runner:
    - name: cloud.profile
    - prof: demo-ubuntu
    - instances: 
      - {{ instance }}
    - vm_overrides:
      minion:
        grains:
          deviceclass: {{ deviceclass }}
          roles: {{ role }}
          zCommandUsername: {{ zCommandUsername }}

"Execute Highstate on new box":
  salt.state:
    - tgt: '{{ instance }}'
    - tgt_type: list
    - highstate: True