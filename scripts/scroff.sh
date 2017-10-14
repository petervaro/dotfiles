#!/bin/bash
## INFO ##
## INFO ##

function revert()
{
    xset dpms 0 0 0;
}

trap revert SIGHUP SIGINT SIGTERM;
xset +dpms dpms 5 5 5;
i3lock -n -b -I 1 -c 000000;
revert;
