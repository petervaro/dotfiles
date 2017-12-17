/* INFO **
** INFO */
import std.file      : readText;
import std.json      : parseJSON;
import std.path      : expandTilde;
import std.regex     : ctRegex, matchFirst;
import std.stdio     : File, writeln, stderr;
import std.array     : Appender, appender;
import std.exception : ErrnoException;
import std.process   : spawnProcess, wait;


/*- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - */
enum
{
    ExitSuccess,
    ExitFailure,
};

/*- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - */
auto pattern = ctRegex!(r"remote\s*(?P<ip>\d+\.\d+\.\d+\.\d+)\s*(?P<port>\d+)");

/*- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - */
immutable helpText = "
NAME
    ufwrules - Set firewall based on the VPN configuration shared with nordvpn

SYNOPSIS
    ufwrules [OPTIONS]

DESCRIPTION
    It is very likely that ufwrules requires elevated privileges because it is
    reading files from the `/etc/openvpn` directory.  But at the same time it is
    also getting the settings from `~/.nordvpn_servers`.  The expansion of the
    tilde character has to be the current user instead of `root`.  So it may has
    to be invoked as:
        $ sudo -E ufwrules

OPTIONS
    -h, --help
        Prints this text.

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
";

/*- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - */
immutable tcp = "tcp";
immutable udp = "udp";


/*----------------------------------------------------------------------------*/
pragma(inline, true):
void addRule(ref string[3][] collected,
             string          location,
             string          index,
             string          port)
{
    auto file = File("/etc/openvpn/client/ovpn_" ~ port ~ "/" ~
                     location ~ index ~ ".nordvpn.com." ~ port ~ ".ovpn", "r");
    scope(exit)
        file.close();

    string line;
    while ((line = file.readln()) !is null)
    {
        auto match = matchFirst(line, pattern);
        if (match)
        {
            collected ~= [match["ip"], match["port"], port];
            break;
        }
    }
}


/*----------------------------------------------------------------------------*/
int main(string[] argv)
{
    /* Handle arguments */
    if (argv.length > 1)
    {
        if (argv[1] == "-h" ||
            argv[1] == "--help")
        {
            writeln(helpText);
            return ExitSuccess;
        }
        else
        {
            stderr.writeln("Invalid flag: ", argv[1]);
            return ExitFailure;
        }
    }

    /* Collect rules from configuration */
    string[3][] rules;
    rules.length = 256;
    immutable servers = parseJSON(readText(expandTilde("~/.nordvpn_servers")));
    foreach (_, locations; servers.object)
        foreach (location, indices; locations.object)
            foreach (_, index; indices.array)
            {
                addRule(rules, location, index.str, tcp);
                try
                    addRule(rules, location, index.str, udp);
                catch (ErrnoException)
                    continue;
            }

    /* Reset all rules */
    wait(spawnProcess(["sudo", "ufw", "reset"]));

    /* Deny everything */
    wait(spawnProcess(["sudo", "ufw", "default", "deny", "outgoing"]));
    wait(spawnProcess(["sudo", "ufw", "default", "deny", "incoming"]));

    /* Allow communication with the router */
    wait(spawnProcess(["sudo", "ufw", "allow", "from", "192.168.1.1/24"]));

    /* Allow communication through the VPN tunnel */
    wait(spawnProcess(["sudo", "ufw", "allow", "out", "on", "tun0"]));
    wait(spawnProcess(["sudo", "ufw", "allow", "in", "on", "tun0"]));

    /* Allow to connect to selected NordVPN servers */
    foreach (ref rule; rules)
        wait(spawnProcess(["sudo", "ufw", "allow", "out", "to", rule[0],
                           "port", rule[1], "proto", rule[2]]));

    /* Report back to the user */
    wait(spawnProcess(["sudo", "ufw", "status", "verbose"]));

    return ExitFailure;
}
