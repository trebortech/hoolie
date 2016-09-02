{% if data['data']['change'] is defined %}
{% set mymessage = 'The *' + data['data']['path'] + '* on machine *' + data['data']['id'] + '* has changed' %}

{% elif 'service' in data['tag'] %}
{% set mymessage = data['data']  %}

{% else %}
{% set mymessage = data['data']['event'] + ' ' + data['data']['name'] %}
{% endif %}

'Slack notify':
  local.state.sls:
    - tgt: 'master1'
    - expr_form: compound
    - arg:
      - slack.blast
    - kwarg:
        pillar:
          mymessage: {{ mymessage }}