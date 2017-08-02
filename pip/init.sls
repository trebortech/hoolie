
"Python Pip":
  pkg.installed:
    - name: python-pip

"Update PIP":
  cmd.run:
    - name: 'pip install --upgrade pip'
    - require:
      - pkg: 'Python Pip'
