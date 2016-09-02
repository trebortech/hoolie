
"Site 1":
  file.recurse:
    - name: /demo/web/site1
    - source: salt://sites/site1
    - user: root
    - group: root
    - order: 12000
