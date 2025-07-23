#!/usr/bin/env python3

import sys
from netmiko import ConnectHandler
import re

# Device credentials
device = {
  "device_type": "hp_procurve",
  "ip": sys.argv[1],
  "username": sys.argv[2],
  "password": sys.argv[3],
}


net_connect = ConnectHandler(**device)
net_connect.enable()

# Step 1: Get all VLAN IDs
vlan_output = net_connect.send_command("show vlan")

# Extract VLAN IDs using regex
vlan_ids = re.findall(r"^\s*(\d{1,4})\s+\S+", vlan_output, re.MULTILINE)
vlan_ids.pop(0)

commands = []

for vlan_id in vlan_ids:
  net_connect.send_command_timing("configure")
  output = net_connect.send_command_timing(f"no vlan {vlan_id}")
  if "Do you want to continue" in output:
      output += net_connect.send_command_timing("y")
  net_connect.send_command_timing("exit")

net_connect.save_config()

net_connect.disconnect()
