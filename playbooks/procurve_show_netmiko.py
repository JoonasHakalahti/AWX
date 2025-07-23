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

def parse_vlan_ports_from_table(vlan_detail):
    tagged_ports = []
    untagged_ports = []

    # Matches lines like:
    # 1                Tagged   Learn        Down
    # 4                Untagged Learn        Down
    port_lines = re.findall(r"^\s*(\S+)\s+(Tagged|Untagged)", vlan_detail, re.MULTILINE)

    for port, mode in port_lines:
        if mode == "Tagged":
            tagged_ports.append(port)
        elif mode == "Untagged":
            untagged_ports.append(port)

    return tagged_ports, untagged_ports



# Connect to the switch
net_connect = ConnectHandler(**device)
net_connect.enable()

# Step 1: Get all VLAN IDs
vlan_output = net_connect.send_command("show vlan")

# Extract VLAN IDs using regex
vlan_ids = re.findall(r"^\s*(\d{1,4})\s+\S+", vlan_output, re.MULTILINE)
print(f"Found VLANs: {vlan_ids}")

# Step 2: For each VLAN, get port assignments
vlan_port_mapping = {}

for vlan_id in vlan_ids:
    vlan_detail = net_connect.send_command(f"show vlan {vlan_id}")
    tagged_ports, untagged_ports = parse_vlan_ports_from_table(vlan_detail)

    vlan_port_mapping[vlan_id] = {
        "tagged": tagged_ports,
        "untagged": untagged_ports,
    }

# Print summary
for vlan_id, ports in vlan_port_mapping.items():
    print(f"\nVLAN {vlan_id}")
    print(f"  Tagged Ports  : {', '.join(ports['tagged']) or 'None'}")
    print(f"  Untagged Ports: {', '.join(ports['untagged']) or 'None'}")

# Close connection
net_connect.disconnect()
