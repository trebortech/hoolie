# Install apache / httpd

{% if grains['os_family'] == 'RedHat' %}
    {% set httpd = 'httpd' %}

{% elif grains['os_family'] == 'Debian' %}
    {% set httpd = 'apache2' %}

{% endif %}


"Install apache / httpd":
  pkg.installed:
    - name: {{ httpd }}


"Restart HTTPD service":
  cmd.wait:
    - name: 'sudo service httpd restart'
    - use_vt: True
    - watch:
      - pkg: "Install apache / httpd"

"Confirm service starts":
  service.enabled:
    - name: {{ httpd }}
    - watch:
      - pkg: "Install apache / httpd"