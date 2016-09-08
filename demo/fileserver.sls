
include:
  - aws.boto
  - nginx

"Deploy fileserver config":
  file.managed:
    - name: '/etc/nginx/sites-available/fileserver'
    - source: salt://demo/files/fileserver

"Remove symlink for Default NGINX":
  file.absent:
    - name: /etc/nginx/sites-enabled/default

"Create symlink for fileserver config":
  file.symlink:
    - name: /etc/nginx/sites-enabled/fileserver
    - target: /etc/nginx/sites-available/fileserver
    - watch:
      - file: "Deploy fileserver config"

"Restart after new fileserver config":
  service.running:
    - name: nginx
    - enable: True
    - reload: True
    - watch:
      - file: "Deploy fileserver config"

"Deploy S3 files":
  s3plus.exists:
    - bucket: saltme-demo
    - path: /x
    - files:
      - SQLEXPR_x64_ENU.zip
      - SQLEXPR_x64_ENU.zip.md5
      - SSMS-Setup-ENU.exe
      - SSMS-Setup-ENU.exe.md5
      - Salt-Minion-2016.3.2-AMD64-Setup.exe
      - zabbix_agents_2.2.9.win.zip
      - zabbix_agents_2.2.9.win.zip.md5
      - zabbix_agents_2.4.4.win.zip
      - zabbix_agents_2.4.4.win.zip.md5