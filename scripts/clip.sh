#!/bin/bash
## INFO ##
## INFO ##

# Set copy and paste functions
if [ -z "$DISPLAY" ];
then
    TMP_FILE='/tmp/clip_sh_tmp_file'
    function copy()
    {
        tee "$TMP_FILE" > /dev/null;
    }

    function paste()
    {
        cat "$TMP_FILE";
    }
else
    function copy()
    {
        tee | xclip -selection clipboard;
    }

    function paste()
    {
        xclip -selection clipboard -o;
    }
fi;

# Handle arguments
if [ -z "$1" ];
then
    paste;
else
    case $1 in
        -c | --copy)
            copy;;
        -p | --paste)
            paste;;
        *)
            printf "Unknown flag\n";
            exit 1;;
    esac;
fi;

