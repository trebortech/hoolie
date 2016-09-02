{% set url = pillar.get('url', 'http://i.giphy.com/FB7yASVBqPiFy.gif') %}
{% set keyword = pillar.get('keyword', 'Kickasdf Minion') %}
{% set lambdahost = pillar.get('lambdahost', 'docker-aws1') %}

{% if lambdahost == 'docker-aws1' %}
/usr/share/nginx/html/aws.html:
  file.managed:
    - source: salt://sites/SaltConf16/aws.html
    - template: jinja
    - defaults:
        gif: {{ url }}
        keyword: {{ keyword }}
{% elif lambdahost == 'docker-linode1' %}
/usr/share/nginx/html/linode.html:
  file.managed:
    - source: salt://sites/SaltConf16/linode.html
    - template: jinja
    - defaults:
        gif: {{ url }}
        keyword: {{ keyword }}
{% endif %}