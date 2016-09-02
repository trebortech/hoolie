# Use existing script

"Deploy SCCM":
  cmd.script:
    - source: salt://demo/files/sccm.bat
    - creates: "c:\\salt\\var\\sccm.txt"
