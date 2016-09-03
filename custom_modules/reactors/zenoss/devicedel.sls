{% if data['data']['deviceclass'] is defined %}

{% set deviceclass = data['data']['deviceclass'] %}
{% set devicename = data['data']['devicename'] %}
{% set serialnumber = data['data']['serialnumber'] %}
{% set title = data['data']['title'] %}

{% endif %}

'Add device to Zenoss':
  runner.zenoss.add_device:
    - deviceName: {{ devicename }}
    - deviceClass: {{ deviceclass }}
    - title: {{ title }}
    - serialNumber: {{ serialnumber }}
