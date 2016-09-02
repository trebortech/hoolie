#ACME Site Deployment

{% if grains['os_family'] == 'RedHat' %}
{% set httpd = 'httpd' %}

{% elif grains['os_family'] == 'Debian' %}
{% set httpd = 'apache2' %}
{% endif %}


# Deploy web content for ACME
"ACME":
  file.recurse:
    - name: /var/www/acme
    - source: salt://sites/acme


"Update Server Name to ACME":
  file.replace:
    - name: /var/www/acme/index.html
    - pattern: 'SITE_NAME'
    - repl: 'ACME'
    - backup: False

"Update Minion Name for ACME":
  file.replace:
    - name: /var/www/acme/index.html
    - pattern: 'MINION_NAME'
    - repl: {{ grains['id'] }}
    - backup: False


# Deploy Site 1 Configuration file
"ACME apache config file":
  file.managed:
    - name: /etc/httpd/conf.d/acme.conf
    - source: salt://poc/acme.conf
    - makedirs: True
    - mode: 600


# Restart httpd service if configuration file updated

"Restart HTTPD service":
  cmd.wait:
    - name: 'sudo service {{ httpd }} restart'
    - use_vt: True
    - watch:
      - file: "ACME apache config file"