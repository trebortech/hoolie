

"Send message to hipchat that demo is done":
  hipchat.send_message:
    - room_id: {{ pillar['hipchat']['room_id'] }}
    - message: 'My docker demo is done {{ grains['id'] }}'
    - from_name: '{{ grains['id'] }}'
    - api_version: {{ pillar['hipchat']['api_version'] }}
    - api_key: {{ pillar['hipchat']['api_key'] }}