{% set workingminion = pillar.get('minionid', '') %}


{% set siteip = salt['mine.get'](tgt=workingminion, fun='weburl', expr_form='glob') %}


"Check deployed site":
  checks.http:
    - name: 'http://{{ siteip[workingminion][0] }}'
    - status: 200
    - fire_event: 'http/check/succeeded/{{ workingminion }}'
