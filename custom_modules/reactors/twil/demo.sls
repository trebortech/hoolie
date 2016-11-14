{% set hal = False %}
{% if "world" in data['body'] %}
{% set mymessage = "I'm sorry, Rob. I'm afraid I can't do that." %}
{% set hal = True %}
{% elif data['images'][0] is defined %}
{% set mymessage = "Message from: *" + data['from'] + "* --> *" + data['body'] + "* " + data['images'][0] %}
{% else %}
{% set mymessage = "Message from: *" + data['from'] + "* --> *" + data['body'] + "*" %}
{% endif %}

{% if hal %}
'Alert Zenny':
  local.state.sls:
    - tgt: "zenny"
    - expr_form: compound
    - arg:
      - zenny.message
    - kwarg:
        pillar:
          color: 'red'
          message: "{{ mymessage }}"

{% else %}
'Slack notify':
  local.state.sls:
    - tgt: 'master1'
    - expr_form: compound
    - arg:
      - slack.blast
    - kwarg:
        pillar:
          mymessage: "{{ mymessage }}"
{% endif %}
