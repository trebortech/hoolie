{% if grains['os_family'] == 'RedHat' %}
    {% set sshd = 'sshd' %}

{% elif grains['os_family'] == 'Debian' %}
    {% set sshd = 'ssh' %}

{% endif %}

"Update ChallengeResponseAuthentication":
  file.replace:
    - name: '/etc/ssh/sshd_config'
    - pattern: 'ChallengeResponseAuthentication yes'
    - repl: 'ChallengeResponseAuthentication no'
    - backup: False

"Update PrintMotd":
  file.replace:
    - name: '/etc/ssh/sshd_config'
    - pattern: 'PrintMotd no'
    - repl: 'PrintMotd yes'
    - backup: False

"Update UsePAM":
  file.replace:
    - name: '/etc/ssh/sshd_config'
    - pattern: 'UsePAM no'
    - repl: 'UsePAM yes'
    - backup: False

"Update PasswordAuthentication":
  file.replace:
    - name: '/etc/ssh/sshd_config'
    - pattern: 'PasswordAuthentication no'
    - repl: 'PasswordAuthentication yes'
    - backup: False

"Restart SSHD service":
  cmd.wait:
    - name: 'sudo service {{ sshd }} restart'
    - use_vt: True
    - watch:
      - file: "Update ChallengeResponseAuthentication"
      - file: "Update PrintMotd"
      - file: "Update UsePAM"
      - file: "Update PasswordAuthentication"