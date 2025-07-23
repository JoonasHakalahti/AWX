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
interfaces = sys.argv[5].split(',')
tag_status= sys.argv[6]
commands = []


for intf in interfaces:
    commands.append(f'vlan {vlan_id}')
    commands.append(f'{tag_status} {intf}')
    commands.append("exit")

net_connect = ConnectHandler(**device)
output = net_connect.send_config_set(commands, delay_factor=2)
net_connect.save_config()
print(output)

net_connect.disconnect()