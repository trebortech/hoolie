
"Update to basic sudoers":
  file.managed:
    - name: /etc/sudoers
    - source: salt://sudoer/basic