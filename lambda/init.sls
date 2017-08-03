

include:
  - docker

"Download corp image":
  dockerng.image_present:
    - name: 'saltme/lambda:v2'
    - require:
      - pip: "Docker Python API"

"lambdacode":
  file.recurse:
    - name: /code
    - source: salt://lambdacode
    - user: root
    - group: root

"Set grain value":
  grains.present:
    - name: 'lambda'
    - value: 'True'

