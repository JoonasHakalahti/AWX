#!/usr/bin/env python3

import sys
from netmiko import ConnectHandler

device = {
  "device_type": "hp_procurve",
  "ip": sys.argv[1],
  "username": sys.argv[2],
  "password": sys.argv[3],
}

vlan_id = sys.argv[4]
vlan_name = sys.argv[5]

net_connect = ConnectHandler(**device)

config_commands = [
    f"vlan {vlan_id}",
    f"name {vlan_name}",
]
output = net_connect.send_config_set(config_commands)
print(output)

net_connect.save_config()  # optional
print(net_connect.send_command("show vlan"))

net_connect.disconnect()
