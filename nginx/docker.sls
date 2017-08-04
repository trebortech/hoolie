

include:
  - docker
  - sites.site1

"Download corp image":
  dockerng.image_present:
    - name: 'saltme/nginx:0.6'
    - require:
      - pip: "Docker Python API"

"Spin up a container":
  dockerng.running:
    - name: Container1
    - image: saltme/nginx:0.6
    - hostname: web1
    - tty: True
    - interactive: True
    - ports:
      - 80/tcp
    - binds:
      - /demo/web/site1:/usr/share/nginx/html:ro
    - port_bindings:
      - 7999:80/tcp
    - dns:
      - 8.8.8.8
      - 8.8.4.4
    - require:
      - dockerng: "Download corp image"

