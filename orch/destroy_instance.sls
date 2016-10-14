{% set instance = pillar.get('name', 'noname') %}

"Destroy instance":
  salt.runner:
    - name: cloud.destroy
    - instances: 
      - {{ instance }}