## INFO ##
## INFO ##

# Constants
VPN_CONF_CLIENT_FILE='/tmp/client-conf.ovpn';
VPN_CONF_STOP_DNS_LEAK='\n# Prevent DNS leaking\n'
VPN_CONF_STOP_DNS_LEAK+='setenv PATH /usr/bin\n';
VPN_CONF_STOP_DNS_LEAK+='script-security 2\n';
VPN_CONF_STOP_DNS_LEAK+='up /etc/openvpn/update-resolv-conf\n';
VPN_CONF_STOP_DNS_LEAK+='down /etc/openvpn/update-resolv-conf\n\n';

VPN_CONF_INDEX='^[0-9]$';

VPN_CONF_INFIX='nordvpn.com';
VPN_CONF_TCP='tcp443';
VPN_CONF_UDP='udp1194';
VPN_CONF_SUFFIX='ovpn';

# Servers
VPN_CONF_STD_0='at6';
VPN_CONF_STD_1='fi1';
VPN_CONF_STD_2='fi2';
VPN_CONF_STD_3='hu1';
VPN_CONF_STD_4='hu2';
VPN_CONF_STD_5='is2';
VPN_CONF_STD_6='is3';
VPN_CONF_STD_7='ro4';
VPN_CONF_STD_8='ch6';
VPN_CONF_STD_9='dk2';

VPN_CONF_TOR_0='lv-tor1';
VPN_CONF_TOR_1='se-tor1';

VPN_CONF_P2P_0='at3';
VPN_CONF_P2P_1='at5';
VPN_CONF_P2P_2='nl2';
VPN_CONF_P2P_3='nl3';
VPN_CONF_P2P_4='ro3';
VPN_CONF_P2P_5='pl3';
VPN_CONF_P2P_6='se1';
VPN_CONF_P2P_7='se2';
VPN_CONF_P2P_8='ch3';
VPN_CONF_P2P_9='ch5';

# Set variables based on arguments
INDEX='0';
SERVER='VPN_CONF_STD_';
VPN_CONF_PORT="$VPN_CONF_TCP";

while true;
do
    case "$1" in
        -S | --std)
            SERVER='VPN_CONF_STD_';;
        -T | --tor)
            SERVER='VPN_CONF_TOR_';;
        -P | --p2p)
            SERVER='VPN_CONF_P2P_';;
        -I | --index)
            shift;
            if [ -z "$1" ];
            then
                printf "Missing index value\n";
                exit 1;
            fi;
            if ! [[ $1 =~ $VPN_CONF_INDEX ]];
            then
                printf "Invalid index value\n";
                exit 1;
            fi;
            INDEX="$1";;
        -t | --tcp)
            VPN_CONF_PORT=VPN_CONF_TCP;;
        -u | --udp)
            VPN_CONF_PORT=VPN_CONF_UDP;;
        -*)
            printf "Unknown flag: $1\n";
            exit 1;;
        *) # No more arguments
            break;;
    esac;
    shift;
done;

VPN_CONF_SERVER="$SERVER$INDEX";
VPN_CONF_SERVER="${!VPN_CONF_SERVER}";
if [ -z "$VPN_CONF_SERVER" ];
then
    VPN_CONF_SERVER="$SERVER""0";
    VPN_CONF_SERVER="${!VPN_CONF_SERVER}";
fi;

# Create temporary configuration
VPN_CONF_CLIENT="$VPN_CONF_SERVER.$VPN_CONF_INFIX.$VPN_CONF_PORT.$VPN_CONF_SUFFIX";
cat "/etc/openvpn/$VPN_CONF_CLIENT" > "$VPN_CONF_CLIENT_FILE";
printf "$VPN_CONF_STOP_DNS_LEAK" >> "$VPN_CONF_CLIENT_FILE";

# Start VPM service
printf "Connecting to: $VPN_CONF_CLIENT\n";
sudo openvpn "$VPN_CONF_CLIENT_FILE";

