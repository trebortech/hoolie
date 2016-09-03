{% set commit = data['post']['commits'] %}
{% set author = commit[0]['author']['name'] %}
{% set commitmessage = commit[0]['message'] %}
{% set branch = data['post']['ref'] %}
{% set refid = data['post']['after'] %}
{% set committime = data['post']['head_commit']['timestamp'] %}
{% set sitename = "coolsite" %}
{% set nodename = data['post']['repository']['name'] + "--" + refid[0:10]  %}

{% set mymessage = "*" + author + "* has just pushed a commit to *" + branch + "* with the following commit message *" + commitmessage + "*" %}

'Slack notify':
  local.state.sls:
    - tgt: 'saltmaster'
    - expr_form: compound
    - arg:
      - slack.blast
    - kwarg:
        pillar: 
          mymessage: "{{ mymessage }}"

{% if branch == 'refs/heads/dev' %}

'Deploy to test bed':
  runner.state.orchestrate:
    - mods: orch.acme
    - pillar:
        sitename: {{ sitename }}
        nodename: {{ nodename }}
        refid: {{ refid }}
        committime: {{ committime }}

{% endif %}
