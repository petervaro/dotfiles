## INFO ##
## INFO ##

tmux new-session -s 'mini-display'

tmux new-window   -n 'lsupd|clock|glances' lsupdates
tmux split-window -v -l 7  -t 0 glances
tmux split-window -h -p 50 -t 0 clock

tmux -c "new-session -s 'mini-display';new-window -n 'lsupd|clock|glances' lsupdates;split-window -v -l 7  -t 0 glances;split-window -h -p 50 -t 0 clock"
