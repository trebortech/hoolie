
# Example of including another file

include:
  - .init

"HA Proxy configuation file for basic demo":
  file.managed:
    - name: /etc/haproxy/haproxy.cfg
    - source: salt://haproxy/basic_config
    - require:
      - file: /etc/default/haproxy
      - pkg: haproxy
    - watch_in:
      - service: haproxy
