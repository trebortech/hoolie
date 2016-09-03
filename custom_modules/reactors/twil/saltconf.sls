{% set keyword =  data['data']['texts'][0]['body'] %}

"react with ":
  runner.lambda_events.update_giphy:
    - keyword: {{ keyword }}
