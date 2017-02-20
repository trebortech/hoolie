"Sync all custom modules":
  module.run:
    - name: saltutil.sync_all

"Create a minion for me":
  event.send:
    - name: 'salt/job/alert/{{ grains.get('id', '') }}'
    - data:
      publicip: {{ grains.get('public_ip', 'noip') }}
    - require:
      - module: "Sync all custom modules"

