{% set profile = pillar.get('profile', '') %}  #ubuntu
{% set lab = pillar.get('lab', '') %}   # lab1
{% set masterip = pillar.get('masterip', '') %}  #65.65.65.65
{% set zonename = pillar.get('zonename', 'salt.trebortech.ninja') %}

# instance ---> labminion#
"Deploy New Lab Minion":
  salt.runner:
    - name: cloud.profile
    - prof: {{ profile }}
    - instances:
      - {{ lab }}minion
    - vm_overrides:
      minion:
        master: {{ masterip }}
        grains:
          roles:
            - labminion
      tag:
        'Environment': 'Lab'
        'Customer': 'ACME'

"Create default user":
  salt.state:
    - tgt: {{ lab }}minion
    - sls:
      - demo.lab.user
      - demo.lab.ssh

"Setup DNS record in Route53":
  salt.runner:
    - name: aws_route53.create_dns_record
    - url: "{{ lab }}master.{{ zonename }}"
    - ip: {{ masterip }}
    - zonename: "{{ zonename }}."
    - recordtype:  "A"
    - ttl: 300