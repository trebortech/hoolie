
{% if grains['os_family'] == 'RedHat' %}
{% set osversion = 'centos' %}

{% elif grains['os_family'] == 'Debian' %}
{% set osversion = 'ubuntu' %}

{% endif %}


include:
  - pip

"Inotify setup":
  pip.installed:
    - name: pyinotify
    - upgrade: True

"Update to basic sudoers":
  file.managed:
    - name: /etc/sudoers
    - source: salt://sudoer/basic-{{ osversion }}

