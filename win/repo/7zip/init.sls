7zip:
  9.20.00.0:
    installer: 'salt://files/7zip/7z920-x64.msi'
    full_name: '7-Zip 9.20 (x64 edition)'
    reboot: False
    install_flags: ' /q '
    msiexec: True
    uninstaller: 'salt://files/7zip/7z920-x64.msi'
    uninstall_flags: ' /qn'
  9.38.00.0:
    installer: 'salt://files/7zip/7z938-x64.msi'
    full_name: '7-Zip 9.38 (x64 edition)'
    reboot: False
    install_flags: ' /q '
    msiexec: True
    uninstaller: 'salt://files/7zip/7z938-x64.msi'
    uninstall_flags: ' /qn'