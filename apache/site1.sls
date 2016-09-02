


# Deploy web content for site 1
"Site 1":
  file.recurse:
    - name: /var/www/site1
    - source: salt://sites/site1

# Deploy Site 1 Configuration file
"Site 1 apache config file":
  file.managed:
    - name: /etc/httpd/conf.d/site1.conf
    - source: salt://apache/site1.conf
    - makedirs: True
    - mode: 600


# Restart httpd service if configuration file updated

"Restart HTTPD service":
  cmd.wait:
    - name: 'sudo service httpd restart'
    - use_vt: True
    - watch:
      - file: "Site 1 apache config file"
