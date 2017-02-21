{% set profile = pillar.get('profile', '') %}

{% set labs = ['lab30', 'lab31', 'lab32', 'lab33'] %}

{% for lab in labs %}
"Deploy New {{ lab }} Server":
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

"Sync modules for {{ lab }}":
  salt.state:
    - tgt: {{ lab }}master
    - sls:
      - sync

"Send event to create minion for {{ lab }}":
  salt.state:
    - tgt: {{ lab }}master
    - sls:
      - demo.lab.createminion
      - demo.lab.user
      - demo.lab.ssh
{% endfor %}