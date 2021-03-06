
#Add device to Zenoss based off grains
# deviceclass


"Add device to Zenoss":
  event.send:
    - name: zenoss/add/device
    - data:
        deviceclass: {{ grains['deviceclass'] }} 
        title: {{ grains['id'] }}
        devicename: {{ grains['fqdn_ip4'][0] }}
        serialnumber: {{ grains['serialnumber'] }}
        zCommandUsername: {{ grains['zCommandUsername'] }}
        serviceorganizer: {{ grains['serviceorganizer'] }}
        servicename: {{ grains['servicename'] }}

