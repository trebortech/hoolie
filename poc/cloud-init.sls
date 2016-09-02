# Configure all of the salt-cloud default files


"Push the cloud provider example files":
  file.recurse:
    - name: /etc/salt/cloud.providers.d
    - source: salt://filestore/cloud.providers.d
    - user: root
    - group: root

"Push the cloud profile example files":
  file.recurse:
    - name: /etc/salt/cloud.profiles.d
    - source: salt://filestore/cloud.profiles.d
    - user: root
    - group: root

"Push the cloud maps example files:":
  file.recurse:
    - name: /etc/salt/cloud.maps.d
    - source: salt://filestore/cloud.maps.d
    - user: root
    - group: root

"Push the cloud support files ":
  file.recurse:
    - name: /etc/salt/cloud.files.d
    - source: salt://filestore/cloud.files.d
    - user: root
    - group: root