####################################
#
# Configure IIS Web Sites
#
####################################

# Stage site files
"Site1":
  file.recurse:
    - name: 'c:\stage'
    - source: salt://iis/files/site1


# Create Application Pool
"Create Test Application Pool":
  win_iis.create_apppool:
    - name: 'TAMU Application Pool'
    - require:
      - win_servermanager: "Install IIS Resources"

{% set sites = [
        {'name':'Test', 'protocol': 'http', 'sourcepath': 'c:\stage', 'port': '82'},
        {'name':'Test Site 2', 'protocol': 'http', 'sourcepath': 'c:\stage', 'port': '83'},
        ] %}


{% for site in sites %}
{{ site.name }}_site:
  win_iis.deployed:
    - name: {{ site.name }}
    - protocol: {{ site.protocol }}
    - sourcepath: {{ site.sourcepath }}
    - port: {{ site.port }}
    - apppool: 'TAMU Application Pool'
    - require:
      - win_iis: "Create Test Application Pool"
      - file: "Site1"

{% endfor %}

