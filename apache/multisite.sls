
{% set sites = [
    {'name': 'Site 1', 'src_files': 'site1', 'config_file': 'site1'},
    {'name': 'Site 2', 'src_files': 'site2', 'config_file': 'site2'}
    ] %}

{% if grains['os_family'] == 'RedHat' %}
{% set config_path = '/etc/httpd/conf.d/' %}

{% elif grains['os_family'] == 'Debian' %}
{% set config_path = '/etc/apache2/sites-enabled/' %}

{% endif %}

{% for site in sites %}
"{{ site.name }} site files deploy":
  file.recurse:
    - name: /var/www/{{ site.src_files }}
    - source: salt://sites/{{ site.src_files }}

"{{ site.name }} apache config file":
  file.managed:
    - name: {{ config_path }}{{ site.config_file }}.conf
    - source: salt://apache/{{ site.config_file }}.conf
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

{% endfor %}


