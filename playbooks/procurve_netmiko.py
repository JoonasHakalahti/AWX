#!/usr/bin/env python3
import sys
from netmiko import ConnectHandler

device = {
    "device_type": "hp_procurve",
    "ip": sys.argv[1],
    "username": sys.argv[2],
    "password": sys.argv[3],
}

net_connect = ConnectHandler(**device)
print(net_connect.send_command("show vlan"))
net_connect.disconnect()
