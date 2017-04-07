

{% if grains['os_family'] == 'RedHat' %}
{% set username = "root" %}
{% elif grains['os_family'] == 'Debian' %}
{% set username = "ubuntu" %}
{% endif %}

'Add zenoss key to {{ username }} user':
  ssh_auth.present:
    - user: {{ username }} 
    - source: salt://ssh_keys/zenoss.id_rsa.pub
    - config: '%h/.ssh/authorized_keys'