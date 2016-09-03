{% if data['data']['message'] is defined %}

{% set message = data['data']['message'] %}
{% set devicename = data['id'] %}
{% endif %}

'Add device to Zenoss':
  runner.zenoss.send_event:
    - kwarg:
        summary: {{ message }}
        device: {{ devicename }}
        severity: 'Info'