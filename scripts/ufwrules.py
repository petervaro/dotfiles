#!/usr/bin/env python3
## INFO ##
## INFO ##

"""
NAME
    ufwrules - Set firewall based on the VPN configuration shared with startvpn

AUTHOR
    Written by Peter Varo.

LICENSE
    Copyright (C) 2017 Peter Varo

    This program is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the Free
    Software Foundation, either version 3 of the License, or (at your option)
    any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT
    ANYWARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
    FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
    details.

    You should have received a copy of the GNU General Public License along with
    this program, most likely a file in the root directory, called 'LICENSE'. If
    not, see http://www.gnu.org/licenses.
"""

# Import python modules
from re import search
from sys import exit, path
from subprocess import run
from os.path import expanduser

# Import dotfiles modules
path.append(expanduser('~/.scripts'))
from vpnconf import SERVERS

# Mofule level constants
PATH = '/etc/openvpn/client'
PATTERN = r'remote\s*(?P<ip>\d+\.\d+\.\d+\.\d+)\s*(?P<port>\d+)'
RULES = []

def add_rules(location, index):
    for is_udp, port in enumerate(('tcp', 'udp')):
        path = f'{PATH}/ovpn_{port}/{location}{index}.nordvpn.com.{port}.ovpn'
        try:
            with open(path) as file:
                match = search(PATTERN, file.read()).groupdict()
                RULES.append((match['ip'], match['port'], port))
        except FileNotFoundError:
            if not is_udp:
                raise

# Collect rules from configuration
try:
    for locations in SERVERS.values():
        for location, indices in locations.items():
            for index in indices:
                add_rules(location, index)
except Exception as exception:
    print(f'Invalid configuration: {exception}')
    exit(1)

# Reset all rules
run('sudo ufw reset', shell=True)

# Deny everything
run('sudo ufw default deny outgoing', shell=True)
run('sudo ufw default deny incoming', shell=True)

# Allow communication with the router
run('sudo ufw allow from 192.168.1.1/24', shell=True)

# Allow communication through the VPN tunnel
run('sudo ufw allow out on tun0', shell=True)
run('sudo ufw allow in on tun0', shell=True)

# Allow to connect to selected NordVPN servers
for rule in RULES:
    run('sudo ufw allow out to {} port {} proto {}'.format(*rule), shell=True)

# Report back to the user
run('sudo ufw status verbose', shell=True)
