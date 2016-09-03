{% if data['data']['message'] is defined %}

{% set message = data['data']['message'] %}
{% set devicename = data['id'] %}
{% endif %}

"Send event to Zenoss":
  runner.zenoss.send_event:
    - summary: "{{ message }}"
    - device: "{{ devicename }}"
    - severity: "Info"
