
{% set ipaddress = pillar.get('ipaddress', '') %}

"Update secondary IP":
  cmd.run:
    - name: "ip addr add dev eth0 {{ ipaddress }}/24"