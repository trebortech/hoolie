{% set profile = pillar.get('profile', '') %}
{% set lab = pillar.get('lab', '') %}

"Deploy New Lab Server":
  salt.runner:
    - name: cloud.profile
    - prof: {{ profile }}
    - instances:
      - {{ lab }}master
    - vm_overrides:
      minion:
        master: 127.0.0.1
        grains:
          lab: {{ lab }}
          roles:
            - labmaster
      tag:
        'Environment': 'Lab'
        'Customer': 'ACME'

"Sync modules":
  salt.state:
    - tgt: {{ lab }}master
    - sls:
      - sync

"Send event to create minion":
  salt.state:
    - tgt: {{ lab }}master
    - sls:
      - demo.lab.createminion
      - demo.lab.user
      - demo.lab.ssh