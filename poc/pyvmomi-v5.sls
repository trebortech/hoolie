# PyVmomi update

"Python Pip":
  pkg.installed:
    - name: python-pip

"Update PIP":
  cmd.run:
    - name: 'easy_install -U pip'
    - require:
      - pkg: 'Python Pip'

"Load older PyVmomi package":
  pip.installed:
    - name: pyvmomi == 5.5.0.2014.1.1
    - require:
      - cmd: 'Update PIP'