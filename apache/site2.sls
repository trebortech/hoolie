


# Deploy web content for site 2
"Site 2":
  file.recurse:
    - name: /var/www/site2
    - source: salt://sites/site2

# Deploy Site 1 Configuration file
"Site 2 apache config file":
  file.managed:
    - name: /etc/httpd/conf.d/site2.conf
    - source: salt://apache/site2.conf
    - makedirs: True
    - mode: 600


# Restart httpd service if configuration file updated

"Restart HTTPD service for site2":
  cmd.wait:
    - name: 'sudo service httpd restart'
    - use_vt: True
    - watch:
      - file: "Site 2 apache config file"
