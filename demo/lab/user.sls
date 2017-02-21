"Add Lab User":
  user.present:
    - name: labuser
    - fullname: labuser
    - shell: '/bin/bash'
    - password: '$1$RMGwjAU9$TrWN4VNEg3.6aDL2sJkV..'
    - optional_groups:
      - wheel
      - admin
      - sudo