{% set mymessage = "The following number *" + data['from'] + "* sent the following message *" + data['body'] + "*" %}

{% set sitename = "coolsite" %}
{% set nodename = "netspend-twiltest" %}



invoke_orchestrate_file:
  runner.state.orchestrate:
    - mods: coolsite
    - pillar:
        sitename: {{ sitename }}
        nodename: {{ nodename }}


'Notify cloud done':
  local.state.sls:
    - tgt: 'saltmaster'
    - arg:
      - slack.blast
    - kwarg:
        pillar:
          mymessage: "{{ mymessage }}"
