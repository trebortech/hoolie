{% if grains['os_family'] == 'RedHat' %}
{% set pippkg = 'python2-pip' %}
{% elif grains['os_family'] == 'Debian' %}
{% set pippkg = 'python-pip' %}
{% endif %}


"Python Pip":
  pkg.installed:
    - name: {{ pippkg }}

"Update PIP":
  cmd.run:
    - name: 'pip install --upgrade pip'
    - require:
      - pkg: 'Python Pip'
