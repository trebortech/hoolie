
"Python Pip":
  pkg.installed:
    - name: python-pip

"Update PIP":
  cmd.run:
    - name: 'easy_install -U pip'
    - require:
      - pkg: 'Python Pip'
