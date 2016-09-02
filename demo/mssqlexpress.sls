#SQL Express install

{% set fileserver = pillar.get('fileserver', 'http://10.5.1.46/') %}
{% set stage = "c:\stage" %}

'Create stage directory':
  file.directory:
    - name: '{{ stage }}'

'Download MSSQL Express setup file':
  archive.extracted:
    - name: '{{ stage }}\extract'
    - source: {{ fileserver }}SQLEXPR_x64_ENU.zip
    - source_hash: {{ fileserver }}SQLEXPR_x64_ENU.zip.md5
    - archive_format: zip

'Download MSSQL Management setup file':
  file.managed:
    - name: '{{ stage }}\SSMS-Setup-ENU.exe'
    - source: {{ fileserver }}SSMS-Setup-ENU.exe
    - source_hash: {{ fileserver }}SSMS-Setup-ENU.exe.md5

'Stage auto install config':
  file.managed:
    - name: '{{ stage }}\mycustomconfig.ini'
    - source: salt://demo/files/mycustomconfig.ini
    - template: jinja
    - defaults:
        INSTANCENAME: "MyDemoTest"
        INSTANCEID: "AUTOTEST2"
        ADMINACCOUNT: "Administrator"

'Install SQLExpress with config file':
  cmd.run:
    - name: '{{ stage }}\extract\SQLEXPR_x64_ENU\setup.exe /ConfigurationFile={{ stage }}/mycustomconfig.ini'

'Deploy manager':
  cmd.run:
    - name: '{{ stage }}\SSMS-Setup-ENU.exe /q'

