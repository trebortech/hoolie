{% set clustername = "saltstack" %}
{% set port = '9201' %}
{% set es_usr = '/usr/share/elasticsearch' %}
{% set es_etc = '/etc/elasticsearch' %}

"Install ElasticSearch and Kibana":
  pkg.installed:
    - pkgs:
      - openjdk-7-jre

"Install Elastic Search package":
  pkg.installed:
    - sources:
      - elasticsearch: salt://elk/elasticsearch-2.3.3.deb

"Deploy Elastic Search config":
  file.managed:
    - name: {{ es_etc }}/elasticsearch.yml
    - source: salt://elk/elasticsearch.yml
    - user: root
    - group: elasticsearch
    - template: jinja
    - defaults:
        HOSTIP: {{ grains['ipv4'][0] }}
        PORT: {{ port }}
        CLUSTERNAME: {{ clustername }}
        MINIONID: {{ grains['id'] }}


"Install Shield License plugin":
  cmd.run:
    - name: "{{ es_usr }}/bin/plugin install license"

"Install Shield plugin":
  cmd.run:
    - name: "{{ es_usr }}/bin/plugin install shield"


"Manage Shield roles":
  file.managed:
    - name: {{ es_etc }}/shield/roles.yml
    - source: salt://elk/roles.yml
    - user: root
    - group: elasticsearch

"Add users":

# Download kibana
https://download.elastic.co/kibana/kibana/kibana-4.5.1-linux-x64.tar.gz


# 
