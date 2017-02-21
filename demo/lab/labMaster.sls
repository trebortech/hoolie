{% set profile = pillar.get('profile', '') %}
{% set instance = pillar.get('lab', '') %}

"Deploy New Lab Server":
  salt.runner:
    - name: cloud.profile
    - prof: {{ profile }}
    - instances:
      - {{ instance }}
    - vm_overrides:
      minion:
        master: 127.0.0.1
        grains:
          roles:
            - labmaster
      tag:
        'Environment': 'Lab'
        'Customer': 'ACME'

"Send event to create minion":
  salt.state:
    - tgt: {{ instance }}
    - sls:
      - sync

"Send event to create minion":
  salt.state:
    - tgt: {{ instance }}
    - sls:
      - demo.lab.createminion
