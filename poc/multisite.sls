
{% set sites = [
    {'name': 'ACME', 'src_files': 'acme', 'config_file': 'acme'},
    {'name': 'Hoolie', 'src_files': 'hoolie', 'config_file': 'hoolie'}
    ] %}

{% if grains['os_family'] == 'RedHat' %}
{% set config_path = '/etc/httpd/conf.d/' %}

{% elif grains['os_family'] == 'Debian' %}
{% set config_path = '/etc/apache2/sites-enabled/' %}
{% endif %}

{% for site in sites %}

{% if site.src_files|lower in salt['grains.get']('brand', '')|lower%}

"{{ site.name }} site files deploy":
  file.recurse:
    - name: /var/www/{{ site.src_files }}
    - source: salt://sites/{{ site.src_files }}

"{{ site.name }} apache config file":
  file.managed:
    - name: {{ config_path }}{{ site.config_file }}.conf
    - source: salt://poc/{{ site.config_file }}.conf
    - makedirs: True
    - mode: 600

"Update Server Name to {{ site.name }}":
  file.replace:
    - name: /var/www/{{ site.src_files }}/index.html
    - pattern: 'SITE_NAME'
    - repl: {{ site.name }}
    - backup: False

"Update Minion Name for {{ site.name }}":
  file.replace:
    - name: /var/www/{{ site.src_files }}/index.html
    - pattern: 'MINION_NAME'
    - repl: {{ grains['id'] }}
    - backup: False

"Reload HTTPD service after {{ site.name }} deployment":
  cmd.wait:
    - name: 'sudo service httpd reload'
    - use_vt: True
    - watch:
      - file: "{{ site.name }} apache config file"

{% endif %}
{% endfor %}