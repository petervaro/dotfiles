## INFO ##
## INFO ##

GLOBIGNORE=".:..";

CONFIGS='configs'
SCRIPTS='scripts';

# Create symlinks to config files
for f in "$CONFIGS"/*;
do
    fname="$(basename $f)";
    if [ -f ~/."$fname" ] &&
       [ ! -L ~/."$fname" ];
    then
        printf "Removing existing file: '~/.$fname'\n";
        rm -f ~/."$fname";
    fi;
    printf "Installing symlink as '~/.$fname'\n";
    ln -sf "$(readlink -e $f)" ~/."$fname";
done;

# Create symlinks to config folders

# Create symlink to user-defined scripts
if [ -d ~/"$SCRIPTS" ] &&
   [ ! -L ~/"$SCRIPTS" ];
then
    printf "Removing existing directory: '~/$SCRIPTS'\n";
    rm -rf ~/"$SCRIPTS";
fi;
printf "Installing symlink as '~/$SCRIPTS'\n";
ln -sf "$(readlink -e $SCRIPTS)" ~/"$SCRIPTS";

