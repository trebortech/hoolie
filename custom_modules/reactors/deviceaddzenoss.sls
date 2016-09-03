{% if data['data']['deviceclass'] is defined %}

{% set deviceclass = data['data']['deviceclass'][0] %}
{% set devicename = data['data']['devicename'][0] %}
{% set serialnumber = data['data']['serialnumber'] %}
{% set title = data['data']['title'] %}

{% endif %}

'Add device to Zenoss':
  runner.zenoss.add_device:
    - kwarg:
        deviceName: {{ devicename }}
        deviceClass: {{ deviceclass }}
        title: {{ title }}
        serialNumber: {{ serialnumber }}