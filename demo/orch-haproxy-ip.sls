# Orchestration 5 Update VIP on haproxy

{% set haproxy = 'demo-haproxy1' %}


"Setup Secondary IP":
  salt.runner:
    - name: haproxy.set_secondary_ip
    - minion: {{ haproxy }}


"Update HAProxy":
  salt.state:
    - tgt: {{ haproxy }}
    - sls:
      - demo.haproxy_config   