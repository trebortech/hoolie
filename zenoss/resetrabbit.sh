#!/bin/bash
rabbitmqctl delete_vhost /zenoss
rabbitmqctl add_vhost /zenoss
rabbitmqctl add_user zenoss zenoss
rabbitmqctl set_permissions -p /zenoss zenoss '.*' '.*' '.*'