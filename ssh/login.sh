#!/bin/bash
#
# This script will be executed *after* all the other init scripts.

# Zenoss Collector system welcome screen

webIP="WebUI http://$(ifconfig eth0 | awk '/inet addr/ {print $2}'| cut -f2 -d:):8888"

read -d '' saasmsg <<_EOF_
  '*********************************************************' \\\n
'**                SaltStack SaaS                       **' \\\n
'**                 version 0.1                         **' \\\n
'**                                                     **' \\\n
'**        Copyright (C) 2016 SaltStack Inc.            **' \\\n
'**             All Rights Reserved                     **' \\\n
'*********************************************************' \\\n
\\\n
$webIP\\\n
\\\\n
'************** NO LOCAL LOGIN IS ALLOWED ***************' \\\n
_EOF_


echo -e $saasmsg > /etc/issue.net;
echo -e $saasmsg > /etc/issue;

