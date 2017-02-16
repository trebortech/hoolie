


"Install SSSD":
  pkg.installed:
    - name: sssd

"Pull default SSSD config in":
  file.managed:
    - source: salt://files/sssd.conf
    - name: '/etc/sssd/sssd.conf'
    - user: root
    - group: root
    - require:
      - pkg: "Install SSSD"


{% if grains['os_family'] == 'Suse' %}

"LDAP config":
  file.managed:
    - source: salt://files/ldap.conf.sles11
    - name: '/etc/ldap.conf'
    - user: root
    - group: root
    - require:
      - pkg: "Install SSSD"

"NSSWITCH install":
  file.managed:
    - source: salt://files/nsswitch.conf-sles11.3
    - name: '/etc/nsswitch.conf'
    - user: root
    - group: root
    - require:
      - pkg: "Install SSSD"

{% endif %}

"Execute Auth":
  cmd.run:
    - name: 'authconfig --enablesssd --enablesssdauth --enablelocauthorize --updateall'
    - stateful: False
    - output_logleve: quiet
    - watch:
      - file: "Pull default SSSD config in"

"Confirm SSSD service started":
  service.running:
    - name: sssd
    - watch:
      - file: "Pull default SSSD config in"



