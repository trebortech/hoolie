# Windows base setup

{% set MID = grains.get('id', 'Nothing') %}

"Set Windows Update Service":
  module.run:
    - name: win_wua.set_wu_settings
    - level: 2
    - msupdate: False
    - day: Wednesday

"Deploy all critical and security updates":
  win_update.installed:
    - categories:
      - 'Critical Updates'
      - 'Security Updates'


"Run basic setup script":
  cmd.script:
    - source: salt://demo/files/winbase.ps1
    - shell: powershell
    - creates: "c:\\salt\\var\\pstest.txt"
    - template: jinja
    - defaults:
        MID: "{{ MID }}"