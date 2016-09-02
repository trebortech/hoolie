"High State Completed":
  event.send:
    - name: 'salt/job/highstate/complete/{{ grains.get('id', '') }}'
    - order: last