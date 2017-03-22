# Docker demo test
{% set ver = 'v1' %}


"Tag new version":
  mc-cloud.cliqrbuild:
    - name: 'Build new cliqrImage'
    - cliqrtagversion: {{ ver }}
    - cliqrtarget: 'root@10.5.1.238'
    - cliqrsourceimage: 'cliqr/worker'