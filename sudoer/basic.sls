

include:
  - pip


"Inotify setup":
  pip.installed:
    - name: pyinotify
    - upgrade: True

"Update to basic sudoers":
  file.managed:
    - name: /etc/sudoers
    - source: salt://sudoer/basic

