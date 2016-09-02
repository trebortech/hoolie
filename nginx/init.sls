######################################################
# Name: nginx
#
# Description: This will install nginx on 
#
# Tested on CentOS 6.5, CentOS 7.1, Ubuntu 14.04
#
######################################################

######################################################
# install the nginx package and make sure the 
# service is running
# 
###################################################### 

"Deploy NGINX package":
  pkg.installed:
    - name: nginx

"Confirm NGINX service started":
  service.running:
    - name: nginx
    - watch:
      - pkg: "Deploy NGINX package"
