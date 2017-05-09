## INFO ##
## INFO ##

# Reset all rules
sudo ufw reset

# Deny everything
sudo ufw default deny outgoing
sudo ufw default deny incoming

# Allow communication with the router
sudo ufw allow from 192.168.1.1/24

# Allow communication through the VPN tunnel
sudo ufw allow out on tun0
sudo ufw allow in on tun0

# Allow to connect to selected NordVPN servers
# at6
sudo ufw allow out to 37.252.190.137 port 443 proto tcp
sudo ufw allow out to 37.252.190.137 port 1194 proto udp

# at3
sudo ufw allow out to 37.252.190.165 port 443 proto tcp
sudo ufw allow out to 37.252.190.165 port 1194 proto udp

# at5
sudo ufw allow out to 37.252.190.132 port 443 proto tcp
sudo ufw allow out to 37.252.190.132 port 1194 proto udp

# ch3
sudo ufw allow out to 91.214.168.69 port 443 proto tcp
sudo ufw allow out to 91.214.168.69 port 1194 proto udp

# ch5
sudo ufw allow out to 136.0.0.90 port 443 proto tcp
sudo ufw allow out to 136.0.0.90 port 1194 proto udp

# ch6
sudo ufw allow out to 82.220.91.139 port 443 proto tcp
sudo ufw allow out to 82.220.91.139 port 1194 proto udp

# dk2
sudo ufw allow out to 82.103.134.5 port 443 proto tcp
sudo ufw allow out to 82.103.134.5 port 1194 proto udp

# fi1
sudo ufw allow out to 91.233.116.223 port 443 proto tcp
sudo ufw allow out to 91.233.116.223 port 1194 proto udp

# fi2
sudo ufw allow out to 185.117.118.161 port 443 proto tcp
sudo ufw allow out to 185.117.118.161 port 1194 proto udp

# hu1
sudo ufw allow out to 79.172.193.211 port 443 proto tcp
sudo ufw allow out to 79.172.193.211 port 1194 proto udp

# hu2
sudo ufw allow out to 217.112.131.74 port 443 proto tcp
sudo ufw allow out to 217.112.131.74 port 1194 proto udp

# is2
sudo ufw allow out to 82.221.139.119 port 443 proto tcp
sudo ufw allow out to 82.221.139.119 port 1194 proto udp

# is3
sudo ufw allow out to 82.221.131.112 port 443 proto tcp
sudo ufw allow out to 82.221.131.112 port 1194 proto udp

# lv-tor1
sudo ufw allow out to 159.148.186.134 port 443 proto tcp
sudo ufw allow out to 159.148.186.134 port 1194 proto udp

# nl2
sudo ufw allow out to 95.211.190.205 port 443 proto tcp
sudo ufw allow out to 95.211.190.205 port 1194 proto udp

# nl3
sudo ufw allow out to 37.48.80.165 port 443 proto tcp
sudo ufw allow out to 37.48.80.165 port 1194 proto udp

# pl3
sudo ufw allow out to 178.250.45.21 port 443 proto tcp
sudo ufw allow out to 178.250.45.21 port 1194 proto udp

# ro3
sudo ufw allow out to 195.254.134.194 port 443 proto tcp
sudo ufw allow out to 195.254.134.194 port 1194 proto udp

# ro4
sudo ufw allow out to 93.115.241.34 port 443 proto tcp
sudo ufw allow out to 93.115.241.34 port 1194 proto udp

# se-tor1
sudo ufw allow out to 95.143.198.80 port 443 proto tcp
sudo ufw allow out to 95.143.198.80 port 1194 proto udp

# se1
sudo ufw allow out to 95.143.198.99 port 443 proto tcp
sudo ufw allow out to 95.143.198.99 port 1194 proto udp

# se2
sudo ufw allow out to 95.143.198.47 port 443 proto tcp
sudo ufw allow out to 95.143.198.47 port 1194 proto udp

# uk28
sudo ufw allow out to 5.152.210.252 port 443 proto tcp
sudo ufw allow out to 5.152.210.252 port 1194 proto udp

# uk36
sudo ufw allow out to 88.150.206.161 port 443 proto tcp
sudo ufw allow out to 88.150.206.161 port 1194 proto udp

# uk54
sudo ufw allow out to 185.145.156.52 port 443 proto tcp
sudo ufw allow out to 185.145.156.52 port 1194 proto udp

# Report back to the user
sudo ufw status verbose
