# Firewall changes for web servers

'Add custom ports for site':
  win_firewall.add_rule:
    - name: 'custom web ports'
    - localport: '443'
    - protocol: tcp
    - action: allow