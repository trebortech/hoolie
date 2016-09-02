####################################
#
# Install IIS Resource
#
####################################


"Install IIS Resources":
  win_servermanager.installed:
    - name: 'Web-Server,Web-Mgmt-Tools,Web-Mgmt-Console,Web-Scripting-Tools'


