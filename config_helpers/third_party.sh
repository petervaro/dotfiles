## INFO ##
## INFO ##

# Install autocrop script
MPV_SCRIPTS=~/.config/mpv/scripts
mkdir -p "$MPV_SCRIPTS";
wget -O "$MPV_SCRIPTS/autocrop.lua" \
     https://raw.githubusercontent.com/mpv-player/mpv/master/TOOLS/lua/autocrop.lua;
