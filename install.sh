## INFO ##
## INFO ##

# Create symlink in home folder
for f in .;
do
    ln -s "$f" "~/.$f";
done;

