
{% set master = pillar.get('master', '') %}

"Update Master Location":
  file.replace:
    - name: '/etc/salt/minion'
    - pattern: 'master: .*'
    - repl: 'master: {{ master }}'
    - backup: False

"Remove old master key":
  file.absent:
    - name: '/etc/salt/pki/minion/minion_master.pub'

"Restart minion":
  cmd.run:
    - name: echo service salt-minion restart | at now + 1 minute