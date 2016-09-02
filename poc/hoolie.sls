#Hoolie Site Deployment
{% if grains['os_family'] == 'RedHat' %}
{% set httpd = 'httpd' %}

{% elif grains['os_family'] == 'Debian' %}
{% set httpd = 'apache2' %}
{% endif %}


# Deploy web content for Hoolie
"Hoolie":
  file.recurse:
    - name: /var/www/hoolie
    - source: salt://sites/hoolie

# Deploy Site 1 Configuration file
"Hoolie apache config file":
  file.managed:
    - name: /etc/httpd/conf.d/hoolie.conf
    - source: salt://poc/hoolie.conf
    - makedirs: True
    - mode: 600


# Restart httpd service if configuration file updated

"Restart HTTPD service":
  cmd.wait:
    - name: 'sudo service {{ httpd }} restart'
    - use_vt: True
    - watch:
      - file: "Hoolie apache config file"