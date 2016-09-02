
"Install HAProxy pkg":
  pkg.installed:
    - name: haproxy

"Stage HAproxy basic files":
  file.managed:
    - name: /etc/default/haproxy
    - source: salt://haproxy/files/default_haproxy
    - require:
      - pkg: haproxy

"Confirm HAproxy service is running":
  service.running:
    - name: haproxy
    - watch:
      - file: /etc/default/haproxy

