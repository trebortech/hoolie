{% set zipversion = pillar.get('version', '9.20.00.0') %}

###############################
#
# maintainer    Robert Booth <rbooth@saltstack.com>
# maturity      new
#
# platform      Windows
# description   Installs the 7Zip ap
# 
###############################

# Install
"Install 7Zip":
  pkg.installed:
    - name: 7zip
    - version: {{ zipversion }}
    - reinstall: True
