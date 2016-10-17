# Orchestration 3 Shutdown all instances

{% set name = pillar.get('name', 'iis') %}



"Destroy Cloud Instances":
  salt.runner:
    - name: cloud.destroy
    - instances:
      - {{ name }}

# Remove them from AD

"Remove Servers from Domain":
  salt.runner:
    - name: ad.unjoin_domain
    - computers:
      - {{ name }}
