

{% set site = "WebApp1" %}
{% set sitefiles = "c:\websites" %}

# Stage site files
"WebApp1 stage files":
  file.managed:
    - name: '{{ sitefiles }}\index.html'
    - source: salt://demo/files/webapp1/index.html
    - template: jinja
    - makedirs: True
    - defaults:
        ID: "{{ grains['id'] }}"

