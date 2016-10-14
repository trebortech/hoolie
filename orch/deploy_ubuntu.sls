
{% set instance = pillar.get('name', 'noname') %}

"Deploy Instance":
  salt.runner:
    - name: cloud.profile
    - prof: demo-ubuntu
    - instances: 
      - {{ instance }}
