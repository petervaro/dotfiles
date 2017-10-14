#!/usr/bin/env python3
## INFO ##
## INFO ##

"""
NAME
    startvpn - NordVPN connection manager

SYNOPSIS
    startvpn [TYPE] [PROTOCOL] --[COUNTRY [INDEX]]

DESCRIPTION
    -h, --help
        Prints this text.

    -l, --list [TYPE] [COUNTRY]
        Lists all possible COUNTRY and INDEX values.
        The result can be filtered by TYPE and COUNTRY.
        Eg. startvpn --list --std --uk

    -s, --std
        Server TYPE: Standard VPN.

    -p, --p2p
        Server TYPE: Peer-to-peer VPN.

    -t, --tor
        Server TYPE: Onion over VPN.

    -d, --dbl
        Server TYPE: Double VPN.

    -D, --dip
        Server TYPE: Dedicated VPN.

    -T, --tcp
        Connection PROTOCOL is TCP.

    -u, --udp
        Connection PROTOCOL is UDP.

    --[COUNTRY [INDEX]]
        Every other flag that starts with double dash will be treated as the
        country code. An integer value between 0 and 9 can follow this flag to
        specify the server. Available country codes and indices can be listed
        via the --list flag.

AUTHOR
    Written by Peter Varo.

LICENSE
    Copyright (C) 2016-2017 Peter Varo

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
from subprocess import run
from os.path import expanduser
from sys import argv, exit, path

# Import dotfiles modules
path.append(expanduser('~/.scripts'))
from vpnconf import SERVERS

# States
location_name  = None
location_index = 0
server_type    = None
server_port    = 'tcp'
list_options   = False

# Handle passed arguments
options = iter(argv[1:])
for option in options:
    # Help
    if option in ('-h', '--help'):
        print(__doc__)
        exit(0)
    # List options
    elif option in ('-l', '--list'):
        list_options = True

    # Standard server
    elif option in ('-s', '--std'):
        server_type = 'std'
    # Peer-to-peer server
    elif option in ('-p', '--p2p'):
        server_type = 'p2p'
    # Onion over VPN server
    elif option in ('-t', '--tor'):
        server_type = 'tor'
    # Double redirection server
    elif option in ('-d', '--dbl'):
        server_type = 'dbl'
    # Dedicated IP server
    elif option in ('-D', '--dip'):
        server_type = 'dip'

    # Use TCP protocol
    elif option in ('-T', '--tcp'):
        server_port = 'tcp'
    # Use UDP protocol
    elif option in ('-u', '--udp'):
        server_port = 'udp'

    # Country
    elif option.startswith('--'):
        location_name = option[2:]
        try:
            location_index = int(next(options))
        except (StopIteration, ValueError, TypeError):
            break

    # Invalid
    else:
        print(f'Invalid flag: {option!r}')
        exit(1)

# List available options
if list_options:
    line = '{0}: {1}: {2}: {1}{3}.nordvpn.com'
    try:
        if server_type is not None:
            server = SERVERS[server_type]
            if location_name is not None:
                for i, index in enumerate(server[location_name]):
                    print(line.format(server_type, location_name, i, index))
            else:
                for location_name, indices in sorted(server.items()):
                    for i, index in enumerate(indices):
                        print(line.format(server_type, location_name, i, index))
        elif location_name is not None:
            previous_type = None
            for server_type, locations in SERVERS.items():
                try:
                    for i, index in enumerate(locations[location_name]):
                        if server_type != previous_type:
                            previous_type = server_type
                            print('-'*80)
                        print(line.format(server_type, location_name, i, index))
                except KeyError:
                    pass
        else:
            previous_type = None
            for server_type, locations in SERVERS.items():
                for location_name, indices in locations.items():
                    for i, index in enumerate(indices):
                        if server_type != previous_type:
                            previous_type = server_type
                            print('-'*80)
                        print(line.format(server_type, location_name, i, index))
    except KeyError as error:
        print(f'Invalid flag: {error!r}')
        exit(1)
    exit(0)

# Set default values if they are not defined
server_type   = server_type   or 'std'
location_name = location_name or 'uk'

# Get server location
try:
    location = (location_name +
                SERVERS[server_type][location_name][location_index])
except (KeyError, IndexError) as error:
    print(f'Invalid flag: {error!r}')
    exit(1)

# Get config path
try:
    folder = {'tcp': 'ovpn_tcp',
              'udp': 'ovpn_udp'}[server_port]
except KeyError as error:
    print(f'Invalid flag: {error!r}')
    exit(1)

# Create config file
config = '/tmp/client-conf.ovpn'
server = f'{location}.nordvpn.com'
with open(f'/etc/openvpn/client/{folder}/'
          f'{server}.{server_port}.ovpn') as original, \
     open(config, 'w') as temporary:
        print(original.read(), file=temporary)
        print('# Prevent DNS leaking',
              'setenv PATH /usr/bin',
              'script-security 2',
              'up /etc/openvpn/update-resolv-conf',
              'down /etc/openvpn/update-resolv-conf',
              sep='\n',
              file=temporary)

# Connect to server
print(f'Connecting to: {server} via {server_port.upper()}')
run(f'sudo openvpn {config}', shell=True)
