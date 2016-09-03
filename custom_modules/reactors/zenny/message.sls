{% set color = data['data']['color'] %}
{% set message = data['data']['message'] %}

'Send Alert':
  local.state.sls:
    - tgt: 'zenny'
    - arg:
      - zenny.message
    - kwarg:
        pillar:
          color: {{ color }}
          message: {{ message }}
