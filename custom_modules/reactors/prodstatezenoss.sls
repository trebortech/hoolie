{% if data['data']['prod_state'] is defined %}

{% set prod_state = data['data']['prod_state'] %}
{% set devicename = data['id'] %}
{% endif %}

'Add device to Zenoss':
  runner.zenoss.set_prod_state:
    - kwarg:
        prod_state: {{ prod_state }}
        device: {{ devicename }}