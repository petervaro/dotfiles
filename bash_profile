#
# ~/.bash_profile
#

# Enable key-pad
setleds -D +num;

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

# Set PS type
export USE_ALTERNATE_COLORED_PROMPT_STRING='';

# Evaluate rc file
[[ -f ~/.bashrc ]] && source ~/.bashrc

# Set timezone variable
export TZ='Europe/London';

# Run custom system initialisation
bash ~/.scripts/sysinit.sh;
