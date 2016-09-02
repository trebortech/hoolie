{% set sitename = pillar['sitename'] %}
{% set nodename = pillar['nodename'] %}
{% set refid = pillar['refid'] %}

"Deploy New Server":
  salt.function:
    - tgt: 'saltmaster'
    - name: cloud.profile
    - kwarg:
        profile: {{ sitename }}
        names:
          - {{ nodename }}
        vm_overrides:
          tag:
            'Environment': 'Testing'
          minion:
            master: 10.5.1.121

"Execute HighState on new test box":
  salt.state:
    - tgt: '{{ nodename }}'
    - highstate: True

"Send cloud deploy message to slack":
  salt.state:
    - tgt: 'saltmaster'
    - sls:
      - slack.blast
    - pillar:
        mymessage: "{{ nodename }} cloud deploy done"

"Send wait message to slack":
  salt.state:
    - tgt: 'saltmaster'
    - sls:
      - slack.blast
    - pillar:
        mymessage: "Application has been deployed. Starting application check from remote host"

"Run check of application deployed":
  salt.state:
    - tgt: 'saltmaster'
    - sls:
      - checks.acme
    - pillar:
        minionid: "{{ nodename }}"

"Send message to slack with status of application":
  salt.state:
    - tgt: 'saltmaster'
    - sls:
      - slack.appstatus
    - pillar:
        funtype: "checks.http"
        minionid: "saltmaster"
        refid: "{{ refid }}"
