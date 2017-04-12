
{% set instance = pillar.get('name', 'noname') %}
{% set deviceclass = pillar.get('deviceclass', '/Server/Linux') %}
{% set zCommandUsername = pillar.get('zCommandUsername', 'ubuntu') %}
{% set serviceorganizer = pillar.get('serviceorganizer', 'None') %}
{% set servicename = pillar.get('servicename', 'None') %}

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
          serviceorganizer: {{ serviceorganizer }}
          servicename: {{ servicename }}

"Execute Highstate on new box":
  salt.state:
    - tgt: '{{ instance }}'
    - tgt_type: list
    - highstate: True