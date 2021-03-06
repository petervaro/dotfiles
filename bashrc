#
# ~/.bashrc
#

# Export variables
export EDITOR=nano;
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib:/usr/lib;
export PATH=$PATH:$HOME/.scripts;
export HISTCONTROL=erasedups;
export HH_CONFIG=hicolor;
export HISTFILESIZE=16384;
export HISTSIZE=${HISTFILESIZE};
export VIRTUAL_ENV_DISABLE_PROMPT=true;
#export PROMPT_COMMAND="history -a; history -n; ${PROMPT_COMMAND}";

# Create aliases
[[ -f ~/.bash_aliases ]] && source ~/.bash_aliases;

# If not running interactively, stop from here
[[ $- != *i* ]] && return;

# If first log in
if [ ! -f /tmp/.already_logged_in ];
then
    # Print system info
    alsi --file-logo=/home/petervaro/.resources/archie --text-color --white;
    touch /tmp/.already_logged_in;
fi;

# Color themes
if [ -n "$USE_ALTERNATE_COLORED_PROMPT_STRING" ];
then
    USER_FG=31;
    USER_BG=41;
    HOST_FG=33;
    HOST_BG=43;
    PATH_FG=32;
    PATH_BG=42;
    GIT_FG=30;
    GIT_BG=47;
    VENV_FG=34;
    VENV_BG=44;
else
    USER_FG=36;
    USER_BG=46;
    HOST_FG=35;
    HOST_BG=45;
    PATH_FG=33;
    PATH_BG=43;
    GIT_FG=30;
    GIT_BG=47;
    VENV_FG=34;
    VENV_BG=44;
fi;

# If running with X
if [ -n "$DISPLAY" ];
then
    TL_CORNER=$'\u250F';
    BL_CORNER=$'\u2517';
    L_HYPHEN=$'\u257A';
    R_HYPHEN=$'\u2578';
    JUNCTION=$'\u2523';
    # Start tmux if not running
    if [ -z "$TMUX" ];
    then
        tmux;
    fi;
# If running without X
else
    TL_CORNER=$'\u250C';
    BL_CORNER=$'\u2514';
    L_HYPHEN=$'\u2500';
    R_HYPHEN=$'\u2500';
    JUNCTION=$'\u251C';
fi;

function virtual_layers()
{
    BRANCH="$(git branch 2>/dev/null | command grep '^*' | colrm 1 2)";
    # Render git-branch if this is a git-repo
    if [ -n "$BRANCH" ];
    then
        printf "\e[0m\n\e[1;${USER_FG}m$JUNCTION\e[37;${GIT_BG}m$R_HYPHEN\e[0;$GIT_FG;${GIT_BG}m$BRANCH";
        # If another virtual layer will follow this
        if [ -n "$VIRTUAL_ENV" ];
        then
            printf "\e[1;37m$L_HYPHEN";
        # If this is the last virtual layer to show
        else
            printf "\e[1;37;${GIT_BG}m:";
            return;
        fi;
    fi;
    # Render virtual-environment if this is one
    if [ -n "$VIRTUAL_ENV" ];
    then
        # If this is the first virtual layer to show
        if [ -z "$BRANCH" ];
        then
            printf "\e[0m\n\e[1;${USER_FG}m$JUNCTION";
        fi;
        printf "\e[0m\e[1;$VENV_FG;${VENV_BG}m$R_HYPHEN\e[37m${VIRTUAL_ENV##*/}\e[1;37m:";
    fi;
}

PS1=$"\[\e[1;$USER_FG;${USER_BG}m\]$TL_CORNER$R_HYPHEN\[\e[37m\]\u";
PS1=$"$PS1\[\e[${USER_FG}m\]$L_HYPHEN\[\e[$HOST_FG;${HOST_BG}m\]$R_HYPHEN\[\e[37m\]\H";
PS1=$"$PS1\[\e[${HOST_FG}m\]$L_HYPHEN\[\e[$PATH_FG;${PATH_BG}m\]$R_HYPHEN\[\e[0;30;${PATH_BG}m\]\w\[\e[1;37m\]:";
PS1=$"$PS1\$(virtual_layers)";
PS1=$"$PS1\[\e[0m\]\n\[\e[1;${USER_FG}m\]$BL_CORNER$R_HYPHEN\[\e[37m\]\\\$\[\e[0m\] ";
export PS1;

# Auto-completion
complete -c man which;

# Window resize
shopt -s checkwinsize;

# Append new history items to .bash_history
#shopt -s histappend;

# Add GPG key to bash profile
export GPG_TTY=$(tty);

