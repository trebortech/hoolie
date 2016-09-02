
# Orchestration 2

# Create groups in AD
# Create users in AD
# Add users to Groups

{% set grouppillarkey = 'demogroups' %}
{% set userpillarkey = 'demousers' %}
{% set saltmaster = 'saltmaster' %}

"Create AD Groups for {{ grouppillarkey }}":
  salt.runner:
    - name: ad.create_secgroups
    - pillarkey: {{ grouppillarkey }}
    - saltmaster: {{ saltmaster }}


"Alert that groups for {{ grouppillarkey }} created":
  salt.state:
    - tgt: {{ saltmaster }}
    - sls:
      - slack.blast
    - pillar:
        mymessage: '{{ grouppillarkey }} has been created in AD'

"Create AD Users for {{ userpillarkey }}":
  salt.runner:
    - name: ad.create_users
    - pillarkey: {{ userpillarkey }}
    - saltmaster: {{ saltmaster }}

"Add users to groups":
  salt.runner:
    - name: ad.add_usertogroup
    - pillarkey: {{ userpillarkey }}
    - saltmaster: {{ saltmaster }}


"Alert that users have been created and added to groups":
  salt.state:
    - tgt: {{ saltmaster }}
    - sls:
      - slack.blast
    - pillar:
        mymessage: 'User and groups for {{ userpillarkey }} has been created in AD'
