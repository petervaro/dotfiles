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
            require_sudo=False,
            pre_require_sudo=False,
            pre_commands=(),
            post_require_sudo=False,
            post_commands=()):

    if pre_commands:
        print('Running pre installation commands:')
        if isinstance(pre_commands, dict):
            pre_commands = pre_commands[variant]
        for commands in pre_commands:
            if pre_require_sudo:
                print('>', SUDO_BIN, *commands)
                run((SUDO_BIN, *commands))
            else:
                print('>', *commands)
                run(commands)

    destination = join(destination_path, destination_name)
    if exists(destination):
        if remove_existing:
            command = ['rm', destination]
            if isfile(destination) or islink(destination):
                print(f'Removing existing file: {destination}')
            elif isdir(destination):
                print(f'Removing existing directory: {destination}')
                command.insert(1, '-r')

            if require_sudo:
                command.insert(0, SUDO_BIN)

            run(command)
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
    command = ['ln', '-s', '-f', source, destination]
    if require_sudo:
        command.insert(0, SUDO_BIN)
    run(command)

    if post_commands:
        print('Running post installation commands:')
        if isinstance(post_commands, dict):
            post_commands = post_commands[variant]
        for commands in post_commands:
            if post_require_sudo:
                print('>', SUDO_BIN, *commands)
                run((SUDO_BIN, *commands))
            else:
                print('>', *commands)
                run(commands)

with open('config.json') as json:
    for node, prefs in load(json):
        try:
            variants = prefs['variants']
            if variant is None:
                print('Variant is required but it is not defined, '
                      f'skipping: {node!r}', file=stderr)
                exit(1)
            try:
                node = variants[variant]
                if node is None:
                    print('Skip installing: variant defined as null')
                    continue
            except KeyError:
                print(f'Invalid variant: {variant!r}, for: {node!r}',
                      file=stderr)
                exit(1)
        except KeyError:
            pass

        pre_commands = prefs.get('pre', {})
        post_commands = prefs.get('post', {})
        install(abspath(node),
                expanduser(prefs['path']),
                prefs.get('name', node),
                remove_existing,
                prefs.get('sudo'),
                pre_commands and pre_commands.get('sudo', False),
                pre_commands and pre_commands.get('commands', ()),
                post_commands and post_commands.get('sudo', False),
                post_commands and post_commands.get('commands', ()))

# Install 3rd party dotfiles
print('Installing 3rd party scripts')
run(('bash', 'third_party.sh'))
