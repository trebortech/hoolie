
# Deploy test files

"Deploy test file":
  file.managed:
    - name: 'c:\\salt\\var\\test.txt'
    - source: salt://demo/files/configs/test.txt
    - makedirs: True


"Deploy test2 file":
  file.managed:
    - name: 'c:\\salt\\var\\test2.txt'
    - source: salt://demo/files/configs/test2.txt
    - makedirs: True
