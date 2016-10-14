# Cool site pulls from
# https://github.com/trebortech/ACME.git

include:
  - nginx

{% set workingdir = "/usr/share/nginx/html/" %}


{% if pillar['version'] is defined %}
{% set env = pillar['version'] %}
{% else %}
{% set env = grains.get('version', 'dev') %}
{% endif %}


####### STAGE KEYS #####################

"Set version grain":
  grains.present:
    - name: version
    - value: {{ env }}


####### PULL IN ACME DEV CODE ##########

"Push ACME site code":
  file.recurse:
    - name: {{ workingdir }}
    - source: salt://ACME
    - saltenv: {{ env }}
    - makedirs: True
    - user: root
    - group: root


"Confirm NGINX service started after git deploy":
  service.running:
    - name: nginx
    - watch:
      - file: "Push ACME site code"

