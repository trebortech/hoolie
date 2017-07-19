# Windows patch upgrade


# KB4025336
"Install windows security patch":
  module.run:
    - name: win_wua.install_update
    - guid: cea5ebc9-b64f-4dc8-9694-4cb6e24b43ee

"Patch requires a reboot":
  module.run:
    - name: system.reboot
