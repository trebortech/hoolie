#
#
# 
#
#
#
#

"Install cmatrix using bash script":
  cmd.script:
    - source: salt://cmatrix/files/cmatrix.sh
    - user: root
    - group: root
    - shell: /bin/bash