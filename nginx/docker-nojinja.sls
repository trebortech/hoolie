
"Download nginx image":
  dockerng.image_present:
    - name: 'saltme/nginx:0.6'
    - require:
      - pip: "Docker Python API"

"Spin up container1":
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
      - 8000:80/tcp
    - dns:
      - 8.8.8.8
      - 8.8.4.4
    - require:
      - dockerng: "Download nginx image"

"Spin up container2":
  dockerng.running:
    - name: Container2
    - image: saltme/nginx:0.6
    - hostname: web2
    - tty: True
    - interactive: True
    - ports:
      - 80/tcp
    - binds:
      - /demo/web/site1:/usr/share/nginx/html:ro
    - port_bindings:
      - 8001:80/tcp
    - dns:
      - 8.8.8.8
      - 8.8.4.4
    - require:
      - dockerng: "Download nginx image"

"Send event to restart HAProxy":
  event.send:
    - name: 'se-team/docker/haproxy/reset'
    - data:
        status: "HA proxy needs to be reset"

