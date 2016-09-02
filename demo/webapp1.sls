####################################
#
# Configure IIS Web Sites
#
####################################

include:
  - iis
  - demo.site1

{% set site = "WebApp1" %}
{% set sitefiles = "c:\websites" %}
{% set stage = "c:\stage" %}
{% set cert = "demo.saltstack.lab.pfx" %}
{% set certhash = "87F7C161C17F4123F9AF4715824FAAAFCD1FABEF" %}
{% set location = "LocalMachine" %}
{% set datastore = "WebHosting" %}

"Deploy certs to IIS machines":
  file.managed:
    - name: '{{ stage }}\{{ cert }}'
    - source: salt://demo/files/{{ cert }}
    - makedirs: True

"Deploy IIS SelfSigned Cert":
  win_certmgr.cert_installed:
    - name: '{{ cert }}'
    - location: '{{ location }}'
    - datastore: '{{ datastore }}'
    - certpath: '{{ stage }}\{{ cert }}'
    - pfx: True

# Create Application Pool
"Create Application Pool":
  win_iis.create_apppool:
    - name: 'Demo Application Pool'
    - require:
      - win_servermanager: "Install IIS Resources"

"Remove default website":
  win_iis.remove_site:
    - name: 'Default Web Site'

"webapp1_site":
  win_iis.deployed:
    - name: '{{ site }}'
    - protocol: 'http'
    - sourcepath: '{{ sitefiles }}'
    - apppool: 'Demo Application Pool'
    - require:
      - win_iis: "Create Application Pool"

"SSL Binding for WebApp1":
  win_certmgr.create_cert_binding:
    - name: {{ site }}
    - site: {{ site }}
    - ipaddress: {{ grains['ipv4'][0] }}
    - location: {{ location }}
    - datastore: {{ datastore }}
    - certhash: {{ certhash }}



