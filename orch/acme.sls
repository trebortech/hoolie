{% set sitename = pillar['sitename'] %}
{% set nodename = pillar['nodename'] %}
{% set refid = pillar['refid'] %}

"Deploy New Server":
  salt.function:
    - tgt: 'saltmaster'
    - name: cloud.profile
    - kwarg:
        profile: {{ sitename }}
        names: {{ nodename }}
        vm_overrides:
          tag:
            'Environment': 'sse-demo'
          minion:
            master: 10.5.1.231

"Execute HighState on new test box":
  salt.state:
    - tgt: '{{ nodename }}'
    - highstate: True

"Send cloud deploy message to slack":
  salt.runner:
    - name: slack.post_message
    - channel: general
    - message: "{{ nodename }} cloud deploy done"
    - from_name: 'Orchestration'


"Send wait message to slack":
  salt.runner:
    - name: slack.post_message
    - channel: general
    - message: "Application has been deployed. Starting application check from remote host"
    - from_name: 'Orchestration'


"Send message to slack with status of application":
  salt.state:
    - tgt: 'saltmaster'
    - sls:
      - slack.appstatus
    - pillar:
        funtype: "checks.http"
        minionid: "saltmaster"
        refid: "{{ refid }}"

#"Destroy VM":
#  salt.function:
#    - tgt: 'saltmaster'
#    - name: cloud.destroy
#    - kwarg:
#        names:
#          - {{ nodename }}

# Need to build tag