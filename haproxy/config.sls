
# Example of including another file

include:
  - .init

"HA Proxy configuation file for docker images":
  file.managed:
    - name: /etc/haproxy/haproxy.cfg
    - source: salt://haproxy/haproxy_docker_config
    - template: jinja
    - require:
      - file: /etc/default/haproxy
      - pkg: haproxy
    - watch_in:
      - service: haproxy
