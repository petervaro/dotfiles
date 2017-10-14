#!/bin/bash
## INFO ##
## INFO ##

# Dependencies
# - scrot
# - imagemagick
# - i3lock

SCREEN_SHOT=/tmp/scrlock.png

trap revert SIGHUP SIGINT SIGTERM;
scrot --multidisp "$SCREEN_SHOT";
convert "$SCREEN_SHOT" -gaussian-blur 0x5 "$SCREEN_SHOT";
i3lock -n -b -I 1 -i "$SCREEN_SHOT";
