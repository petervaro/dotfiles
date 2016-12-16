#
# ~/.bash_profile
#

# If running without X
if [ "$TERM" == "linux" ];
then
    echo -en "\e]P0303640"; # black
    echo -en "\e]P84f5865"; # darkgrey
    echo -en "\e]P1d46c58"; # darkred
    echo -en "\e]P9e39485"; # red
    echo -en "\e]P2a5d557"; # darkgreen
    echo -en "\e]PAc8e795"; # green
    echo -en "\e]P3d5b657"; # brown
    echo -en "\e]PBe7d295"; # yellow
    echo -en "\e]P45891d4"; # darkblue
    echo -en "\e]PC95bbe7"; # blue
    echo -en "\e]P59858d4"; # darkmagenta
    echo -en "\e]PDbf95e7"; # magenta
    echo -en "\e]P658d4cd"; # darkcyan
    echo -en "\e]PE95e7e2"; # cyan
    echo -en "\e]P794a0ac"; # lightgrey
    echo -en "\e]PFf0f0f0"; # white
    clear; # for background artifacting
fi;

# Evaluate rc file
[[ -f ~/.bashrc ]] && . ~/.bashrc

# Run archey on every login
#archey3 --config=.config/archey3.conf;

# Set timezone variable
TZ='Europe/London';
export TZ;

