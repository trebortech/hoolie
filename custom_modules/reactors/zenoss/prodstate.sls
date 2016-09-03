{% if data['data']['prod_state'] is defined %}

{% set prod_state = data['data']['prod_state'] %}
{% set devicename = data['id'] %}
{% endif %}

'Set prod state in Zenoss':
  runner.zenoss.set_prod_state:
    - prod_state: "{{ prod_state }}"
    - device: "{{ devicename }}"
