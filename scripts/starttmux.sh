#!/bin/bash
## INFO ##
## INFO ##

# Set up the right half of the terminal
tmux split-window -h -p 50 \;                                           \
     select-pane -t 1 \;                                                \
     split-window -v -b -l 7 \;                                         \
     split-window -h -l 56 'tty-clock -sctD -C 7' \;                    \
     select-pane -t 1 \;                                                \
     split-window -h -l 52 'python ~/scripts/lsupdates.py' \;           \
     select-pane -t 4 \;                                                \
     split-window -h -p 50 \;                                           \
     split-window -v -p 50 'glances' \;                                 \
     select-pane -t 5 \;                                                \
     split-window -v -p 50 'speedometer -b -s -rx wlp6s0 -tx wlp6s0' \; \
     select-pane -t 5 \;                                                \
     split-window -v -p 50 'prettyping --nolegend google.com' \;        \
     send-keys -t 5 'bash ~/scripts/startvpn.sh -I 8 -P' Enter \;       \
     select-pane -t 4 \;                                                \
     split-window -v -p 50 \;                                           \
     split-window -v -b -l 15 \;                                        \
     send-keys -t 4 'mocp' Enter \;                                     \
     select-pane -t 4 \;                                                \
     split-window -v -l 11 'vis';

# Set up the left half of the terminal
if [ "$1" == '--work' ];
then
    tmux select-pane -t 0 \;                                            \
         split-window -h -p 50 \;                                       \
         split-window -v -b -l 5 'sudo socat tcp-listen:443,reuseaddr,fork tcp:localhost:4430';
fi;
