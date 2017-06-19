"Stage windows powershell bootstrap":
  file.managed:
    - name: "c:\\bootstrap.ps1"
    - source: salt:\\salt\bootstrap.ps1