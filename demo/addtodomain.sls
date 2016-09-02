

"Add computer to AD":
  win_ad.join_domain:
    - name: {{ pillar['ad']['domain'] }}
    - username: {{ pillar['ad']['username'] }}
    - password: {{ pillar['ad']['password'] }}
    - account_ou: 'ou=MyDemoOU,dc=saltstack,dc=lab'
    - restart: True