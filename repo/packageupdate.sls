
{% set packages = pillar.get('packages', {}) %}

"Update to versioned package set":
  pkg.installed:
    - pkgs:
{% for package in packages %}
      {% if package.version is defined %}
      - {{ package.name }}: {{ package.version }}
      {% else %}
      - {{ package.name }}
      {% endif %}
{% endfor %}