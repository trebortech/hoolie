{% set vip = grains.get('vip', '') %}


"Confirm HAproxy service is running":
  service.running:
    - name: haproxy
    - watch:
      - file: "HA Proxy configuation file demo1"

"HA Proxy configuation file demo1":
  file.managed:
    - name: /etc/haproxy/haproxy.cfg
    - source: salt://demo/files/haproxy.config
    - template: jinja
    - defaults:
        VIP: "{{ vip }}"