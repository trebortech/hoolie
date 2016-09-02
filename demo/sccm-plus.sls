"Run CCM install script":
  cmd.script:
    - source: salt://demo/files/sccm-plus.bat
    - template: jinja
    - defaults:
        MP: "tccmgr03p.fnb.fnni.com"
        SMSMP: "TCCMGR03P.fnb.fnni.com"
        SMSSLP: "tccmgr03p.fnb.fnni.com"
        FSP: "tccmgr03p.fnb.fnni.com"
        SMSSITECODE: "CM3"
        CCMHTTPPORT: "4451"