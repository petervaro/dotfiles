## INFO ##
## INFO ##

CONFFILES='conffiles';
CONFDIRS='confdirs';
USERDIRS='scripts resources';

function find_nonvim_files()
{
    printf "$(find $1 ! -iname '*~' -a ! -iname '*.swp')";
}


# Handle arguments
REMOVE=false
for a in "$@";
do
    case "$a" in
        -r | --remove-existing)
            REMOVE=true;;
        -b | --backup-existing)
            REMOVE=false;;
        *)
            printf "Unknown flag\n";
            exit 1;
    esac;
done;


# Create symlinks to config files
for f in $(find_nonvim_files "$CONFFILES");
do
    # If f is a file
    if [ -f "$f" ];
    then
        fname="$(basename $f)";
        # If $HOME has a file with that name
        # and that file in $HOME is not a symlink
        if [ -f ~/."$fname" ] &&
           [ ! -L ~/."$fname" ];
        then
            if [ "$REMOVE" == true ];
            then
                printf "Removing existing file: '~/.$fname'\n";
                rm -f ~/."$fname";
            else
                printf "Saving existing file as: '~/.$fname.bak'\n";
                mv ~/."$fname" ~/."$fname".bak;
            fi;
        fi;
        printf "Installing symlink as '~/.$fname'\n";
        ln -sf "$(readlink -e $f)" ~/."$fname";
    fi;
done;


# Create symlinks to config directories
for d in "$CONFDIRS"/*;
do
    # If d is a directory
    if [ -d "$d" ];
    then
        dname="$(basename $d)";
        # If it is the current directory
        if [ "$dname" == "$CONFDIRS" ];
        then
            continue;
        # If $HOME has a directory with that name
        # and that directory in $HOME is not a symlink
        elif [ -d ~/."$dname" ] &&
             [ ! -L ~/."$dname" ];
        then
            if [ "$REMOVE" == true ];
            then
                printf "Removing existing directory: '~/.$dname'\n";
                rm -rf ~/."$dname";
            else
                printf "Saving existing directory as: '~/.$dname.bak'\n";
                mv ~/."$dname" ~/."$dname".bak;
            fi;
        fi;
        printf "Installing symlink as '~/.$dname'\n";
        ln -sf "$(readlink -e $d)" ~/."$dname";
    fi;
done;


# Create symlink to user-defined scripts
for d in $USERDIRS;
do
    if [ -d ~/."$d" ]
    then
        if [ "$REMOVE" == true ];
        then
            printf "Removing existing directory: '~/.$d'\n";
            rm -rf ~/."$d";
        else
            printf "Saving existing directory as: '~/.$d.bak'\n";
            mv ~/."$d" ~/."$d".bak;
        fi;
    fi;
    printf "Creating new directory: '~/.$d'\n";
    mkdir ~/."$d";

    for f in $(find_nonvim_files "$d");
    do
        # If f is a file
        if [ -f "$f" ];
        then
            fname="$(basename $f)";
            printf "Installing symlink as '~/.$d/$fname'\n";
            ln -sf "$(readlink -e $f)" ~/."$d"/"$fname";
        fi;
    done;
done;

