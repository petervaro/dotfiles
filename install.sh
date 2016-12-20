## INFO ##
## INFO ##

CONFFILES='conffiles';
CONFDIRS='confdirs';
SCRIPTS='scripts';

# TODO: if *.bak files already exist, then start adding .bakN (N is uint)

function find_nonvim_files()
{
    printf "$(find $1 ! -iname '*~' -a ! -iname '*.swp')";
}

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
            printf "Saving existing file as: '~/.$fname.bak'\n";
            mv ~/."$fname" ~/."$fname".bak;
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
            printf "Saving existing directory as: '~/.$dname.bak'\n";
            mv ~/."$dname" ~/."$dname".bak;
        fi;
        printf "Installing symlink as '~/.$dname'\n";
        ln -sf "$(readlink -e $d)" ~/."$dname";
    fi;
done;

# Create symlink to user-defined scripts
if [ -d ~/"$SCRIPTS" ]
then
    printf "Saving existing directory as: '~/$SCRIPTS.bak'\n";
    mv ~/"$SCRIPTS" ~/"$SCRIPTS".bak;
fi;
printf "Creating new directory: '~/$SCRIPTS'\n";
mkdir ~/"$SCRIPTS";

for f in $(find_nonvim_files "$SCRIPTS");
do
    # If f is a file
    if [ -f "$f" ];
    then
        fname="$(basename $f)";
        printf "Installing symlink as '~/$SCRIPTS/$fname'\n";
        ln -sf "$(readlink -e $f)" ~/"$SCRIPTS"/"$fname";
    fi;
done;

