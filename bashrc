#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return;

# Start tmux
if [ -z "$TMUX" ];
then
    tmux;
fi;

# Create aliases
alias ls='ls --color=always';
alias tree='tree -C';
alias nano='nano --smooth --tabsize=4 --autoindent';
alias python3='python';
alias pip3='pip';
alias diff='colordiff';
alias grep='grep --color=always';
alias ping='prettyping';
alias make='colormake';
alias clock='tty-clock -scD -C 7';
alias rand='python $HOME/documents/personal/local/arch-linux/rand/rand.py';
alias midi='fluidsynth -a alsa -m alsa_seq -l -i /usr/share/soundfonts/FluidR3_GM2-2.sf2';
alias sizeof='du -hsx';
alias lsupdates='python $HOME/documents/personal/local/arch-linux/list-updates/lsupdates.py';
alias watchlist='bash $HOME/documents/personal/local/arch-linux/watchlist/watchlist.sh';
alias compile='echo "clang -std=c11 -O3 -v -pedantic -Wall -Wextra" && clang -std=c11 -O3 -v -pedantic -Wall -Wextra';
alias scroff='bash $HOME/documents/personal/local/arch-linux/screen-lock/scroff.sh';
#alias scrlock='';
alias startvpn='sudo openvpn /etc/openvpn/at3.nordvpn.com.tcp443.ovpn';
#is3.nordvpn.com.tcp443.ovpn';
#alias startvpn='sudo openvpn /etc/openvpn/se-tor1.nordvpn.com.udp1194.ovpn';
#lv-tor1.nordvpn.com.tcp443.ovpn';

# Export variables
export EDITOR=vim;
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib:/usr/lib;
export PATH=$PATH:/home/petervaro/.gem/ruby/2.3.0/bin;
export HISTCONTROL=erasedups;

# If running with X
if [ -n "$DISPLAY" ];
then
    PS1=$'\[\e[1;36;46m\]\u250F\u2578\[\e[37m\]\u\[\e[36m\]\u257A\[\e[35;45m\]\u2578\[\e[37m\]\H\[\e[35m\]\u257A\[\e[33;43m\]\u2578\[\e[0;30;43m\]\w\[\e[1;33m\]:\[\e[0m\]\n\[\e[1;36m\]\u2517\u2578\[\e[37m\]\$\[\e[0m\] ';
# If running without X
else
    PS1=$'\[\e[1;36;46m\]\u250C\u2500\[\e[37m\]\u\[\e[36m\]\u2500\[\e[35;45m\]\u2500\[\e[37m\]\H\[\e[35m\]\u2500\[\e[33;43m\]\u2500\[\e[0;30;43m\]\w\[\e[1;33m\]:\[\e[0m\]\n\[\e[1;36m\]\u2514\u2500\[\e[37m\]\$\[\e[0m\] ';
fi;

# Auto-completion
complete -c man which;

# Window resize
shopt -s checkwinsize;

