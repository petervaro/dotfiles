/* INFO **
** INFO */
import std.algorithm.sorting : sort;
import std.conv              : ConvException, parse, to;
import std.exception         : ErrnoException;
import std.file              : readText, FileException;
import std.json              : JSONValue, parseJSON, JSONException, JSON_TYPE;
import std.path              : expandTilde;
import std.process           : spawnProcess, wait, ProcessException;
import std.stdio             : File, stderr, writeln;
import std.uni               : toUpper;
import std.utf               : UTFException;


/*- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - */
enum
{
    ExitSuccess,
    ExitFailure,
};

/*- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - */
immutable helpText = "
NAME
    nordvpn - NordVPN connection manager

SYNOPSIS
    nordvpn [OPTIONS][TYPE][PROTOCOL][--COUNTRY [INDEX]]

OPTIONS
    -h, --help
        Prints this text.

    -l, --list [TYPE] [COUNTRY]
        Lists all possible COUNTRY and INDEX values.
        The result can be filtered by TYPE and COUNTRY.
        Eg.
            nordvpn --list --ch
            nordvpn --list --std --uk

TYPE
    -s, --std
        Standard VPN.

    -p, --p2p
        Peer-to-peer VPN.

    -t, --tor
        Onion over VPN.

    -d, --dbl
        Double VPN.

    -D, --dip
        Dedicated VPN.

PROTOCOL
    -T, --tcp
        Connection uses TCP.

    -u, --udp
        Connection uses UDP.

COUNTRY INDEX
    --** [0-9]
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
";

/*- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - */
immutable preventDnsLeak = "
# Prevent DNS leaking
setenv PATH /usr/bin
script-security 2
up /etc/openvpn/update-resolv-conf
down /etc/openvpn/update-resolv-conf
";

/*- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - */
immutable configPath  = "/tmp/client-conf.ovpn";
immutable serversPath = "~/.nordvpn_servers";


/*----------------------------------------------------------------------------*/
pragma(inline, true):
void writeListLine(const(char[]) serverType,
                   const(char[]) locationName,
                   size_t        relativeIndex,
                   const(char[]) absoluteIndex)
{
    writeln(serverType  ,  ": ",
            locationName,  ": ",
            relativeIndex, ": ",
            locationName, absoluteIndex, ".nordvpn.com");
}


/*----------------------------------------------------------------------------*/
int main(string[] argv)
{
    /* States */
    string locationName;
    byte   locationIndex;
    bool   listOptions;
    string serverType;
    string serverPort = "tcp";

    /* Handle arguments */
    if (argv.length > 1)
    {
        bool nextArgIsLocationIndex;
        foreach (ref arg; argv[1..$])
        {
            /* Positional command line argument */
            if (nextArgIsLocationIndex)
            {
                try
                    locationIndex = parse!byte(arg);
                catch (ConvException error)
                    stderr.writeln(
                        "Invalid index: ", arg, " : ", error.msg,
                        "\n(Run `nordvpn --help` for available options)");
                    return ExitFailure;
            }
            /* Keyword command line argument */
            else
                switch (arg)
                {
                    /* Help */
                    case "-h":
                    case "--help":
                        writeln(helpText);
                        return ExitSuccess;

                    /* List options */
                    case "-l":
                    case "--list":
                        listOptions = true;
                        break;

                    /* Standard server */
                    case "-s":
                    case "--std":
                        serverType = "std";
                        break;

                    /* Peer-to-peer server */
                    case "-p":
                    case "--p2p":
                        serverType = "p2p";
                        break;

                    /* Onion over VPN server */
                    case "-t":
                    case "--tor":
                        serverType = "tor";
                        break;

                    /* Double redirecition server */
                    case "-d":
                    case "--dbl":
                        serverType = "dbl";
                        break;

                    /* Dedicated IP server */
                    case "-D":
                    case "--dip":
                        serverType = "dip";
                        break;

                    /* Use TCP protocol */
                    case "-T":
                    case "--tcp":
                        serverPort = "tcp";
                        break;

                    /* Use UDP protocol */
                    case "-u":
                    case "--udp":
                        serverPort = "udp";
                        break;

                    default:
                        if (arg[0] == '-' &&
                            arg[1] == '-')
                        {
                            locationName = arg[2..$];
                            nextArgIsLocationIndex = true;
                            break;
                        }
                        stderr.writeln(
                            "Invalid option: ", arg,
                            "\n(Run `nordvpn --help` for available options)");
                        return ExitFailure;
                }
        }
    }

    /* Get user configured data from the JSON file */
    JSONValue servers;
    immutable userPath = expandTilde(serversPath);
    try
        servers = parseJSON(readText(userPath));
    catch (FileException error)
    {
        stderr.writeln("Cannot read from file: ", userPath, ": ", error.msg);
        return ExitFailure;
    }
    catch (UTFException error)
    {
        stderr.writeln("Cannot read from file: ", userPath, ": ", error.msg);
        return ExitFailure;
    }
    catch (JSONException error)
    {
        stderr.writeln("Invalid JSON format: ", userPath, ": ", error.msg);
        return ExitFailure;
    }

    /* Sanity check */
    if (servers.type != JSON_TYPE.OBJECT)
    {
        stderr.writeln("Top level type expected to be an Object but got: ",
                       to!string(servers.type), " in ", userPath);
        return ExitFailure;
    }

    /* List available options */
    if (listOptions)
    {
        string[]            names;
        string              previousType;
        bool                noResults = true;
        immutable(char[80]) decorator = '-';

        /* Filter by server type */
        if (serverType)
        {
            if (serverType !in servers)
            {
                stderr.writeln("Undefined server type: \"", serverType,
                               "\"\n(Run `nordvpn --list` for available " ~
                               "locations)");
                return ExitFailure;
            }

            servers = servers[serverType];
            if (servers.type != JSON_TYPE.OBJECT)
            {
                stderr.writeln("Server type expected to be an Object but got: ",
                               to!string(servers.type),
                               " for: \"", serverType,
                               "\" in ", userPath);
                return ExitFailure;
            }

            /* Filter by location */
            if (locationName)
            {
                if (locationName !in servers)
                {
                    stderr.writeln("Undefined server location: \"",
                                   locationName,
                                   "\"\n(Run `nordvpn --list` for available " ~
                                   "locations)");
                    return ExitFailure;
                }

                servers = servers[locationName];
                if (servers.type != JSON_TYPE.ARRAY)
                {
                    stderr.writeln("Server locations expected to be an " ~
                                   "Array but got: ", to!string(servers.type),
                                   " for: \"", locationName,
                                   "\" in ", userPath);
                    return ExitFailure;
                }

                foreach (i, index; servers.array)
                {
                    noResults = false;
                    writeListLine(serverType, locationName, i, index.str);
                }
            }
            /* All locations */
            else
            {
                foreach (name, _; servers.object)
                    names ~= name;
                foreach (ref name; sort(names))
                {
                    if (servers[name].type != JSON_TYPE.ARRAY)
                    {
                        stderr.writeln("Server locations expected to be an " ~
                                       "Array but got: ",
                                       to!string(servers[name].type),
                                       " for: \"", name,
                                       "\" in ", userPath);
                        return ExitFailure;
                    }

                    foreach (i, index; servers[name].array)
                    {
                        noResults = false;
                        writeListLine(serverType, name, i, index.str);
                    }
                }
            }
        }
        /* Filter by location */
        else if (locationName)
        {
            foreach (serverType, locations; servers.object)
            {
                if (locations.type != JSON_TYPE.OBJECT)
                {
                    stderr.writeln("Server type expected to be an Object but " ~
                                   "got: ", to!string(locations.type),
                                   " for: \"", serverType,
                                   "\" in ", userPath);
                    return ExitFailure;
                }
                else if (locationName in locations)
                {
                    if (locations[locationName].type != JSON_TYPE.ARRAY)
                    {
                        stderr.writeln("Server locations expected to be an " ~
                                       "Array but got: ",
                                       to!string(locations[locationName].type),
                                       " for: \"",
                                       locationName,
                                       "\" in ", userPath);
                        return ExitFailure;
                    }

                    foreach (i, index; locations[locationName].array)
                    {
                        noResults = false;
                        if (serverType != previousType)
                        {
                            previousType = serverType;
                            writeln(decorator);
                        }
                        writeListLine(serverType, locationName, i, index.str);
                    }
                }
            }
        }
        /* All server types and locations */
        else
        {
            foreach (serverType, locations; servers.object)
            {
                if (locations.type != JSON_TYPE.OBJECT)
                {
                    stderr.writeln("Server type expected to be an Object but " ~
                                   "got: ", to!string(locations.type),
                                   " for: \"", serverType,
                                   "\" in ", userPath);
                    return ExitFailure;
                }

                names.length = 0;
                foreach (name, _; locations.object)
                    names ~= name;

                foreach (ref name; sort(names))
                {
                    if (locations[name].type != JSON_TYPE.ARRAY)
                    {
                        stderr.writeln("Server locations expected to be an " ~
                                       "Array but got: ",
                                       to!string(locations[name].type),
                                       " for: \"", name,
                                       "\" in ", userPath);
                        return ExitFailure;
                    }

                    foreach (i, index; locations[name].array)
                    {
                        noResults = false;
                        if (serverType != previousType)
                        {
                            previousType = serverType;
                            writeln(decorator);
                        }
                        writeListLine(serverType, name, i, index.str);
                    }
                }
            }
        }
        if (noResults)
            writeln("No servers found in: ", userPath);
        return ExitSuccess;
    }

    /* Set default values if they are not defined */
    serverType = serverType ? serverType : "std";

    /* Get server location */
    if (serverType !in servers)
    {
        stderr.writeln("Undefined server type: \"", serverType,
                       "\"\n(Run `nordvpn --list` for available locations)");
        return ExitFailure;
    }

    immutable(string) locationNumber;
    servers = servers[serverType];
    if (servers.type != JSON_TYPE.OBJECT)
    {
        stderr.writeln("Server type expected to be an Object but got: ",
                       to!string(servers.type),
                       " for: \"", serverType,
                       "\" in ", userPath);
        return ExitFailure;
    }

    locationName = locationName ? locationName : "uk";
    if (locationName !in servers)
    {
        stderr.writeln("Undefined server location: \"", locationName,
                       "\"\n(Run `nordvpn --list` for available locations)");
        return ExitFailure;
    }

    servers = servers[locationName];
    if (servers.type != JSON_TYPE.ARRAY)
    {
        stderr.writeln("Server locations expected to be an Array but got: ",
                       to!string(servers.type),
                       " for: \"", locationName,
                       "\" in ", userPath);
        return ExitFailure;
    }
    else if (locationIndex >= servers.array.length)
    {
        stderr.writeln("Invalid server index: ", locationIndex,
                       "\n(Run `nordvpn --list` for available locations)");
        return ExitFailure;
    }

    immutable server =
        locationName ~ servers[locationIndex].str ~ ".nordvpn.com";

    /* Get stock configuration file */
    immutable originalPath = "/etc/openvpn/client/ovpn_" ~ serverPort ~ "/" ~
                             server ~ "." ~ serverPort ~ ".ovpn";
    File original;
    try
        original = File(originalPath, "r");
    catch (ErrnoException error)
    {
        stderr.writeln("Cannot open file: ", originalPath,
                       "(errno: ", error.errno, ")");
        return ExitFailure;
    }
    scope (exit)
        original.close();

    /* Create custom configuration file */
    File temporary;
    try
        temporary = File(configPath, "w");
    catch (ErrnoException error)
    {
        stderr.writeln("Cannot open file: ", configPath,
                       "(errno: ", error.errno, ")");
        return ExitFailure;
    }
    scope (failure)
        temporary.close();

    /* Copy lines from original to temporary and extend it with extra content */
    string line;
    while ((line = original.readln()) !is null)
        temporary.write(line);
    temporary.writeln(preventDnsLeak);
    temporary.close();

    /* Connect to server */
    writeln("Connecting to: ", server, " via ", toUpper(serverPort));
    try
        wait(spawnProcess(["openvpn", configPath]));
    catch (ProcessException error)
    {
        stderr.writeln("Cannot start process: ", error.msg);
        return ExitFailure;
    }

    return ExitSuccess;
}
