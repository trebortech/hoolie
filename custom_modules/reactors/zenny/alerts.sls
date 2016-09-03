
{% set id = data['id'] %} 

{% if data['fun'] == 'state.highstate' %}
{% if data['retcode'] is defined %}
{% set status = data['retcode'] %}

{% if status == 0 %}

{% set color = 'green' %}
{% set message = 'The highstate for ' + id + ' has completed' %}
  
{% else %}

{% set color = 'red' %}
{% set message = 'The highstate for ' + id + ' had a problem. Please look into the log files' %}

{% endif %}

'Send a status update':
  local.state.sls:
    - tgt: 'zenny'
    - arg:
      - zenny.message
    - kwarg:
        pillar:
          color: {{ color }}
          message: {{ message }}

{% endif %}
{% endif %}
