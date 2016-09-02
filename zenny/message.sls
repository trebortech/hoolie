
{% set color = pillar.get('color', 'clear') %}
{% set message =  pillar.get('message', 'test') %}

"Send me a message":
  zenny.alert:
    - color: "{{ color }}"
    - message: "{{ message }}"