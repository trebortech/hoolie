

"Create a minion for me":
  event.send:
    - name: 'salt/job/alert/{{ grains.get('id', '') }}'
    - data:
      publicip: {{ grains.get('public_ip', 'noip') }}


