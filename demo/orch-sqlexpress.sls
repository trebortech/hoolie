# Orchestration 4 Deploy DB instance

"Deploy DB New Server":
  salt.runner:
    - name: cloud.profile
    - prof: demo-db
    - instances:
        - demo-db1

"Put short pause in for db system to catch up":
  salt.function:
    - tgt: 'saltmaster'
    - name: test.sleep
    - kwarg:
        length: 30

"Deploy initial setup states":
  salt.state:
    - tgt: 'demo-db1'
    - tgt_type: list
    - sls:
      - sync
      - demo.network

wait_for_reboots_db:
  salt.wait_for_event:
    - name: salt/minion/*/start
    - id_list:
      - demo-db1
    - require:
      - salt: "Put short pause in for db system to catch up"


"Send DB Server deployed message to slack":
  salt.state:
    - tgt: 'saltmaster'
    - sls:
      - slack.blast
    - pillar:
        mymessage: "New DB Servers have been deployed"

"Add DB Servers to AD":
  salt.state:
    - tgt: 'demo-db1'
    - sls:
      - demo.addtodomain

"Wait for DB AD add Reboot":
  salt.wait_for_event:
    - name: salt/minion/*/start
    - id_list:
      - demo-db1

"Put short pause in for db system to catch up after AD Add restart":
  salt.function:
    - tgt: 'saltmaster'
    - name: test.sleep
    - kwarg:
        length: 30

"Execute Highstate on DB boxes":
  salt.state:
    - tgt: 'demo-db1'
    - highstate: True

"Send DB server highstate message to slack":
  salt.state:
    - tgt: 'saltmaster'
    - sls:
      - slack.blast
    - pillar:
        mymessage: "Highstate for new DB servers has been executed"

