{% set zipversion = pillar.get('version', '9.20.00.0') %}

###############################
#
# maintainer    Robert Booth <rbooth@saltstack.com>
# maturity      new
# depends       
#               srv/salt/win/repo/7zip/
#
# platform      Windows
# description   Removes the 7Zip ap
# 
###############################

# Install
"Install 7Zip":
  pkg.removed:
    - name: 7zip
    - version: {{ zipversion }}