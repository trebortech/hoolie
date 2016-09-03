{% set mymessage = 'The file on ' + data['data']['id'] + ' contains ' + data['data']['contains'] %}

'Slack notify':
  local.state.sls:
    - tgt: 'saltmaster'
    - expr_form: compound
    - arg:
      - slack.blast
    - kwarg:
        pillar:
          mymessage: {{ mymessage }}

