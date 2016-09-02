# Orchestration 3 Shutdown all instances

{% set grouppillarkey = 'demogroups' %}
{% set userpillarkey = 'demousers' %}
{% set saltmaster = 'saltmaster' %}


"Destroy Cloud Instances":
  salt.runner:
    - name: cloud.destroy
    - instances:
      - demo-iis1
      - demo-iis2
      - demo-db1

# Remove them from AD

"Remove Servers from Domain":
  salt.runner:
    - name: ad.unjoin_domain
    - computers:
      - demo-iis1
      - demo-iis2
      - demo-db1


"Remove AD Users for {{ userpillarkey }}":
  salt.runner:
    - name: ad.remove_users
    - pillarkey: {{ userpillarkey }}
    - saltmaster: {{ saltmaster }}

"Remove AD Groups for {{ grouppillarkey }}":
  salt.runner:
    - name: ad.remove_secgroups
    - pillarkey: {{ grouppillarkey }}
    - saltmaster: {{ saltmaster }}