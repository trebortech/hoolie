# setup the giphy pages
{% set gce_gif = salt['pillar.get']('gce_gif', 'http://i.giphy.com/A3RyFua6XWG76.gif') %}
{% set gce_keyword = salt['pillar.get']('gce_keyword', 'Smiling Minion') %}
{% set aws_gif = salt['pillar.get']('aws_gif', 'http://i.giphy.com/FB7yASVBqPiFy.gif') %}
{% set aws_keyword = salt['pillar.get']('aws_keyword', 'Kick Minion') %}
{% set do_gif = salt['pillar.get']('do_gif', 'http://i.giphy.com/9aNLCal9p9AgE.gif') %}
{% set do_keyword = salt['pillar.get']('do_keyword', 'Laughing Minion') %}
{% set linode_gif = salt['pillar.get']('linode_gif', 'http://i.giphy.com/JunL6dl3Xw3ok.gif') %}
{% set linode_keyword = salt['pillar.get']('linode_keyword', 'Kiss Minion') %}
{% set local_gif = salt['pillar.get']('local_gif', 'http://i.giphy.com/YYO87CDrKfLz2.gif') %}
{% set local_keyword = salt['pillar.get']('local_keyword', 'Waving Minion') %}

nginx:
  pkg:
    - installed
  service:
    - running
    - require:
      - pkg: nginx

/usr/share/nginx/html/:
  file.recurse:
    - source: salt://sites/SaltConf16
    - template: jinja
    - include_empty: True
    - defaults:
        gce_gif: {{ gce_gif }}
        gce_keyword: {{ gce_keyword }}
        aws_gif: {{ aws_gif }}
        aws_keyword: {{ aws_keyword }}
        do_gif: {{ do_gif }}
        do_keyword: {{ do_keyword }}
        linode_gif: {{ linode_gif }}
        linode_keyword: {{ linode_keyword }}
        local_gif: {{ local_gif }}
        local_keyword: {{ local_keyword }}
    - require:
      - pkg: nginx
    - watch_in:
      - service: nginx