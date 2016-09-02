#Install window support files for salt-cloud

# Install winexe

"Install winexe":
  pkg.installed:
    - name: winexe
    - sources:
      - winexe: salt://filestore/winexe_1.00.1-11.1_amd64.deb

"Install Impacket":
  pip.installed:
    - name: impacket