# Install Zabbix  2.2

{% set DBHOST = 'localhost' %}
{% set DBNAME = 'zabbix' %}
{% set DBUSER = 'zabbix' %}
{% set DBPASSWORD = 'zabbix' %}
{% set TZ = 'America/Chicago' %}

# CentOS 6 install

# Install supporting services
"Install mysql server":
  pkg.installed:
    {% if grains['os_family'] == 'RedHat' %}
    - pkgs:
      - mysql-server
      - MySQL-python
    {% elif grains['os_family'] == 'Debian' %}
    - pkgs:
      - mysql-server
      - mysql-client
      - python-mysql.connector
      - python-mysqldb
    {% endif %}

"Allow for remote access":
  file.replace:
    - name: '/etc/my.cnf'
    - pattern: 'bind-address            = 127.0.0.1'
    - repl: 'bind-address            = 0.0.0.0'



"Check mysql service":
  service.running:
    - require:
      - pkg: "Install mysql server"
    - names:
    {% if grains['os_family'] == 'RedHat' %}
      - mysqld
    {% elif grains['os_family'] == 'Debian' %}
      - mysql
    {% endif %}


"Create Zabbix db":
  mysql_database.present:
    - name: {{ DBNAME }}

"Create Zabbix db users":
  mysql_user.present:
    - name: {{ DBUSER }}
    - password: {{ DBPASSWORD }}
    - host: {{ DBHOST }}

"Grant user db access":
  mysql_grants.present:
    - name: {{ DBNAME }}
    - user: {{ DBUSER }}
    - database: {{ DBNAME }}.*
    - grant: all privileges


"Set SELinux mode to permissive":
  selinux.mode:
    - name: permissive

# Install rpm
# rpm -ivh http://repo.zabbix.com/zabbix/2.2/rhel/6/x86_64/zabbix-release-2.2-1.el6.noarch.rpm

"Install Zabbix repository package":
  pkg.installed:
    - sources:
      - zabbix-release: salt://zabbix/zabbix-release-2.2-1.el6.noarch.rpm
    - require:
      - selinux: "Set SELinux mode to permissive"

# Install zabbix service

"Install Zabbix services":
  pkg.installed:
    - pkgs:
      - zabbix-agent
      - zabbix-web-mysql
      - zabbix-server-mysql

"Stage file for mysql":
  file.managed:
    - name: /tmp/zabbix-init.sql
    - source: salt://zabbix/zabbix-init.sql

# Import initial schema and data
"Import initial schema and data":
  cmd.run:
    - name: "mysql -uroot zabbix < /tmp/zabbix-init.sql"
    - require:
      - file: "Stage file for mysql"

"Deploy Zabbix server config":
  file.managed:
    - name: /etc/zabbix/zabbix_server.conf
    - source: salt://zabbix/zabbix_server.conf
    - mode: 640
    - user: {{ DBUSER }}
    - group: root
    - template: jinja
    - defaults:
        DBHOST: {{ DBHOST }}
        DBNAME: {{ DBNAME }}
        DBUSER: {{ DBUSER }}
        DBPASSWORD: {{ DBPASSWORD }}


"Updated PHP Setup":
  file.managed:
    - name: /etc/httpd/conf.d/zabbix.conf
    - source: salt://zabbix/zabbix.conf
    - mode: 644
    - user: root
    - group: root
    - template: jinja
    - defaults:
        TZ: {{ TZ }}

"Restart apache after new Zabbix config":
  service.running:
    - name: httpd
    - enable: True
    - reload: True
    - watch:
      - file: "Updated PHP Setup"

"Restart Zabbix after new Zabbix config":
  service.running:
    - name: zabbix-server
    - enable: True
    - reload: True
    - watch:
      - file: "Deploy Zabbix server config"


# Update iptables
"Add IP Tables rule for webserver":
  iptables.insert:
    - table: filter
    - position: 1
    - chain: INPUT
    - jump: ACCEPT
    - match: state
    - connstate: NEW
    - dport: 80
    - sport: 1025:65535
    - proto: tcp
    - save: True
