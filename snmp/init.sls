

# Install snmpd
"SNMPD Package installed":
  pkg.installed:
    - pkgs:
      - snmp
      - snmpd

# configure snmp.conf file
"Configured SNMP conf file":
  file.managed:
    - name: /etc/snmp/snmpd.conf
    - source: salt://snmp/snmpd.conf
    - user: root
    - group: root
    - mode: 400

"Confirm SNMPD service started":
  service.running:
    - name: snmpd
    - watch:
      - file: "Configured SNMP conf file"