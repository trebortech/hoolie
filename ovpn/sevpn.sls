
{% set workingpath = '/etc/openvpn' %}
{% set caname = 'sedemo-vpn' %}
{% set vpnname = 'vpn-server' %}
{% set vpnnet = '10.77.0.0' %}
{% set localnet = '10.11.0.0' %}
{% set vpnendpoint = 'seovpn.salt.trebortech.ninja' %}
{% set users = ['rbooth-salt-mac'] %}


"Install OpenVPN":
  pkg.installed:
    - name: openvpn

"DHKey deployed":
  cmd.run:
    - name: "openssl dhparam -out {{ workingpath }}/dh2048.pem 2048"
    - unless: "test -e {{ workingpath }}/dh2048.pem"

"SE VPN":
  ovpn.ca:
    - name: {{ caname }}
    - cacert_path: {{ workingpath }}
    - days: 3650
    - C: 'US'
    - ST: 'Texas'
    - L: 'Round Rock'
    - O: 'SaaS'
    - emailAddress: 'noreply@acme.com'

"SE VPN Users":
  ovpn.user:
    - name: {{ caname }}
    - workingpath: {{ workingpath }}
    - CN:
      - {{ vpnname }}
      {% for user in users %}
      - {{ user }}
      {% endfor %}

"Push OpenVPN configuration":
  file.managed:
    - name: '{{ workingpath }}/local-vpn.conf'
    - source: salt://ovpn/files/ovpn.conf
    - mode: 400
    - user: root
    - group: root
    - template: jinja
    - defaults:
        WORKINGPATH: {{ workingpath }}
        CANAME: {{ caname }}
        CERT: {{ vpnname }}
        VPNNET: {{ vpnnet }}
        LOCALNET: {{ localnet }}

{% for user in users %}
"Client Configuration for {{ user }}":
  file.managed:
    - name: '{{ workingpath}}/{{ caname }}/{{ user }}/{{ caname }}-vpn.ovpn'
    - source: salt://ovpn/files/ovpn-client.conf
    - mode: 400
    - user: root
    - group: root
    - template: jinja
    - defaults:
        VPNENDPOINT: {{ vpnendpoint }}
        CANAME: {{ caname }}
        USERNAME: {{ user }}

"Copy CA Cert to {{ user }} directory":
  file.copy:
    - name: '{{ workingpath }}/{{ caname }}/{{ user }}/{{ caname }}_ca_cert.crt'
    - source: '{{ workingpath }}/{{ caname }}/{{ caname }}_ca_cert.crt'

"Build tar file for {{ user }}":
  cmd.run:
    - name: "tar -czf {{ workingpath }}/{{ caname }}/{{ user }}.tgz {{ workingpath }}/{{ caname }}/{{ user }}"
    - unless: "test -e {{ workingpath }}/{{ caname }}/{{ user }}.tgz"


{% endfor %}
