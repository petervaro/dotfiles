## INFO ##
## INFO ##

from json       import load
from os         import remove, rename, renames, removedirs, symlink, makedirs
from os.path    import isdir, isfile, islink, join, expanduser, abspath, exists
from re         import split, compile
from subprocess import run
from sys        import argv, exit, stderr

SUDO_BIN = '/usr/bin/sudo'

variant = None
remove_existing = False

# Handle arguments
try:
    argv = iter(argv[1:])
    # TODO: Implement -c, --compile flags to re/compile binaries
    for arg in argv:
        if arg in ('-r', '--remove'):
            remove_existing = True
        elif arg in ('-b', '--backup'):
            remove_existing = False
        elif arg in ('-v', '--variant'):
            try:
                variant = next(argv)
            except StopIteration:
                print('Variant value is not defined', file=stderr)
                exit(1)
        else:
            print(f'Unknown flag: {arg!r}', file=stderr)
            exit(1)
except IndexError:
    pass

def install(source,
            destination_path,
            destination_name,
            remove_existing,
            require_sudo=False):
    destination = join(destination_path, destination_name)
    if exists(destination):
        if remove_existing:
            if isfile(destination) or islink(destination):
                print(f'Removing existing file: {destination}')
                if require_sudo:
                    run((SUDO_BIN, 'rm', destination))
                else:
                    remove(destination)
            elif isdir(destination):
                print(f'Removing existing directory: {destination}')
                if require_sudo:
                    run((SUDO_BIN, 'rm', '-r', destination))
                else:
                    removedirs(destination)
        else:
            if isfile(destination):
                print(f'Saving existing file as: {destination}.old')
                if require_sudo:
                    run((SUDO_BIN, 'mv', destination, f'{destination}.old'))
                else:
                    rename(destination, f'{destination}.old')
            elif isdir(destination):
                print(f'Saving existing directory as: {destination}.old')
                if require_sudo:
                    run((SUDO_BIN, 'mv', destination, f'{destination}.old'))
                else:
                    renames(destination, f'{destination}.old')
    else:
        makedirs(destination_path, exist_ok=True)
    print(f'Installing symlink as: {destination}')
    if require_sudo:
        run((SUDO_BIN, 'ln', '-s', source, destination))
    else:
        symlink(source, destination)

with open('config.json') as json:
    for node, prefs in load(json).items():
        try:
            variants = prefs['variants']
            if variant is None:
                print('Variant is required but it is not defined, '
                      f'skipping: {node!r}')
                continue
            try:
                node = variants[variant]
            except KeyError:
                print(f'Invalid variant: {variant!r}, for: {node!r}')
                continue
        except KeyError:
            pass

        install(abspath(node),
                expanduser(prefs['path']),
                prefs.get('name', node),
                remove_existing,
                prefs.get('sudo'))
