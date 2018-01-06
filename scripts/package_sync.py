## INFO ##
## INFO ##

from datetime    import datetime
from itertools   import islice, zip_longest
from json        import load
from os          import listdir
from os.path     import join, expanduser, isfile
from subprocess  import run, Popen, PIPE
from sys         import argv, exit, stderr

SYNC_PATH   = expanduser('~/.package_sync')
DATE_FORMAT = '%Y-%m-%d-%H-%M-%S'
HEAD_NAME   = '__HEAD__'

ARGV    = iter(islice(argv, 1, None))
DRY_RUN = False
VARIANT = None

#------------------------------------------------------------------------------#
def _execute_transaction(transaction_json, transaction_name):
    for transaction in transaction_json[transaction_name]:
        pipe = False
        # If single command
        if 'command' in transaction:
            parameters = transaction.get('parameters', [])
            if isinstance(parameters, str):
                parameters = transaction_json['references'][parameters]
            commands = [transaction['command'] + parameters]
        # If multiple commands
        elif 'commands' in transaction:
            pipe = transaction.get('pipe')
            commands = transaction['commands']
        # No commands to execute
        else:
            continue

        # Check for variants
        variants = transaction.get('variants')
        if (VARIANT is not None and
            variants is not None and
            VARIANT not in variants):
                continue
        # Check if dry-run
        elif DRY_RUN:
            if pipe:
                print('$', ' | '.join(' '.join(c) for c in commands))
            else:
                for command in commands:
                    print('$', *command)
        # Execute command
        else:
            if pipe:
                stdout = None
                for command in commands:
                    process = Popen(command, stdin=PIPE, stdout=PIPE)
                    stdout = process.communicate(input=stdout)[0]
                    process.stdout.close()
            else:
                for command in commands:
                    run(command)


#------------------------------------------------------------------------------#
def _sorted_file_names(reverse):
    file_names = {}
    for file_name in listdir(SYNC_PATH):
        if file_name == HEAD_NAME:
            continue
        file_names[datetime.strptime(file_name[:-5], DATE_FORMAT)] = file_name

    return [file_name for _, file_name in sorted(file_names.items(),
                                                 key=lambda i: i[0],
                                                 reverse=reverse)]


#------------------------------------------------------------------------------#
def help():
    print("""
NAME
    package_sync - Synchronise states of multiple Arch Linux installations

SYNOPSIS
    package_sync [OPTIONS]

DESCRIPTION
    Although pacman and pacaur are very easy yet extremely powerful tools to use
    on Arch Linux to maintain the system, it can be quite cumbersome to do the
    same kind of installations across multiple systems.  This utility keeps
    track of the different states of the system, making it very easy to go back
    and forth between them.

OPTIONS
    -h, --help
        Prints this text.

    -n, --new editor
        Opens a new file in the given editor with the name of the current date
        and time.

    -l, --last editor
        Opens the last file created (not necessarily the HEAD) in the given
        editor.

    -s, --set file
        Overrides the HEAD to point at the given file name.  The file name shall
        not contain any path information, just the file name and the extension,
        eg. 2017-12-12-19-44-30.json.  This command should be used carefully, as
        it is not executing any transactions, therefore package_sync can easily
        get into an invalid state.

    -q, --query
        Shows all the transaction files and indicating which one is the HEAD.

    -v, --variant variant
        Specify subset of transactions that should be executed.

    -V, --validate
        Validates the transaction files.

    -u, --upgrade
        Executes all files created after the current HEAD.

    -d, --downgrade [step]
        Executes step number of files before the current HEAD.  If step is not
        given it defaults to 1.

    -D, --dry
        Dry run.

TRANSACTION

    Each transaction file shall be a valid JSON one.  The top-level object shall
    be an Object, which must have the following keys:
        - upgrade
        - downgrade

    The corresponding values of these keys are Arrays of Objects.  Each of these
    Objects must have the following keys:
        - command
    and may have the following keys:
        - parameters
        - variants

    The top-level Object may have the following keys:
        - references

    Example:
    {
        "references":
        {
            "new":
            [
                "package-1",
                "package-2
            ],
            "old":
            [
                "package-0"
            ]
        },
        "upgrade":
        [
            {
                "command": ["sudo", "pacman", "-Rns", "another-package"]
            },
            {
                "command": ["sudo", "pacman", "-Rns"],
                "parameters":
                [
                    "this-package",
                    "that-package"
                ]
            },
            {
                "command": ["sudo", "pacman", "-Rns"],
                "parameters": "old",
                "variants":
                [
                    "computer-1"
                ]
            },
            {
                "command": ["sudo", "pacman", "-S", "--needed"],
                "parameters": "new"
            }
        ],
        "downgrade":
        [
            {
                "command": ["sudo", "pacman", "-Rns"],
                "parameters": "new"
            },
            {
                "command": ["sudo", "pacman", "-S", "--needed"],
                "parameters": "old",
                "variants":
                [
                    "computer-1"
                ]
            },
            {
                "command": ["sudo", "pacman", "-S", "--needed"],
                "parameters":
                [
                    "this-package",
                    "that-package"
                ]
            },
            {
                "command":
                [
                    "sudo", "pacman", "-S", "--needed", "another-package"
                ]
            }
        ]
    }

AUTHOR
    Written by Peter Varo.

LICENSE
    Copyright (C) 2017 Peter Varo

    This program is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the Free
    Software Foundation, either version 3 of the License, or (at your option)
    any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT
    ANYWARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
    FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
    details.

    You should have received a copy of the GNU General Public License along with
    this program, most likely a file in the root directory, called 'LICENSE'. If
    not, see http://www.gnu.org/licenses.
""")


#------------------------------------------------------------------------------#
def new(editor):
    """
    Create a new transaction file
    """
    if editor is None:
        print('Missing positional argument: editor', file=stderr)
        exit(1)

    command = editor, join(SYNC_PATH,
                           f'{datetime.now().strftime(DATE_FORMAT)}.json')
    if DRY_RUN:
        print('$', *command)
    else:
        run(command)
    return True


#------------------------------------------------------------------------------#
def last(editor):
    """
    Open last transaction file
    """
    if editor is None:
        editor = 'cat'

    file_names = _sorted_file_names(reverse=True)
    if not file_names:
        print('No transaction file found in: {SYNC_PATH}')
        exit(0)

    command = editor, join(SYNC_PATH, file_names[0])
    if DRY_RUN:
        print('$', *command)
    else:
        run(command)
    return True


#------------------------------------------------------------------------------#
def set_(file_name):
    """
    Set head to given file without executing any transactions
    """
    if file_name is None:
        print('Missing positional argument: file name', file=stderr)
        exit(1)

    if not isfile(join(SYNC_PATH, file_name)):
        print(f'Not a file: {join(SYNC_PATH, file_name)}', file=stderr)
        exit(1)

    if DRY_RUN:
        print(f'$ echo {file_name!r} > {join(SYNC_PATH, HEAD_NAME)}')
    else:
        with open(join(SYNC_PATH, HEAD_NAME), 'w') as head:
            head.write(file_name)
    return True


#------------------------------------------------------------------------------#
def query():
    """
    List all transaction from oldest to youngest
    """
    try:
        with open(join(SYNC_PATH, HEAD_NAME)) as head:
            head_file = head.read()
    except FileNotFoundError:
        head_file = None

    for file_name in _sorted_file_names(reverse=False):
        print(file_name,
              end=' [HEAD]\n' if file_name == head_file else '\n')
    return True


#------------------------------------------------------------------------------#
def validate():
    """
    Vaildates all transaction files (as in being true JSON files)
    """
    for file_name in _sorted_file_names(reverse=False):
        try:
            with open(join(SYNC_PATH, file_name)) as json:
                load(json)
        except Exception as error:
            print(f'Validation failed for {file_name!r}: {error}')
    return True


#------------------------------------------------------------------------------#
def upgrade():
    """
    Execute all transactions since the current HEAD
    """
    head_path = join(SYNC_PATH, HEAD_NAME)

    if not isfile(head_path):
        open(head_path, 'a').close()

    with open(head_path, 'r+') as head:
        file_name = head_file = head.read()

        execute_transaction = False if head_file else True
        for file_name in _sorted_file_names(reverse=False):
            if execute_transaction:
                with open(join(SYNC_PATH, file_name)) as json:
                    _execute_transaction(load(json), 'upgrade')
            elif file_name == head_file:
                execute_transaction = True

        if not DRY_RUN:
            head.seek(0)
            head.write(file_name)
            head.truncate()
    return True


#------------------------------------------------------------------------------#
def downgrade(counter):
    """
    Execute n transactions before the current HEAD
    """
    head_path = join(SYNC_PATH, HEAD_NAME)

    if not isfile(head_path):
        print('HEAD is not set. Try --upgrade or --set')
        exit(1)

    with open(join(SYNC_PATH, HEAD_NAME), 'r+') as head:
        file_name = head_file = head.read()

        try:
            counter = int(counter)
        except Exception:
            counter = 1

        execute_transaction = False
        for file_name in _sorted_file_names(reverse=True):
            if file_name == head_file:
                execute_transaction = True
            if execute_transaction:
                if not counter:
                    break
                with open(join(SYNC_PATH, file_name)) as json:
                    _execute_transaction(load(json), 'downgrade')
                counter -= 1

        if not DRY_RUN:
            head.seek(0)
            head.write(file_name)
            head.truncate()
    return True


#------------------------------------------------------------------------------#
def dry():
    global DRY_RUN
    DRY_RUN = True


#------------------------------------------------------------------------------#
def variant(variant):
    if variant is None:
        print('Missing positional argument: variant', file=stderr)
        exit(1)
    global VARIANT
    VARIANT = variant


#------------------------------------------------------------------------------#
if __name__ == '__main__':
    callbacks = {'-h'          : (help, 0, 99),
                 '-help'       : (help, 0, 99),
                 '--help'      : (help, 0, 99),
                 'help'        : (help, 0, 99),
                 '-n'          : (new, 1, 99),
                 '--new'       : (new, 1, 99),
                 '-s'          : (set_, 1, 99),
                 '--set'       : (set_, 1, 99),
                 '-l'          : (last, 1, 99),
                 '--last'      : (last, 1, 99),
                 '-u'          : (upgrade, 0, 99),
                 '--upgrade'   : (upgrade, 0, 99),
                 '-d'          : (downgrade, 1, 99),
                 '--downgrade' : (downgrade, 1, 99),
                 '-V'          : (validate, 0, 99),
                 '--validate'  : (validate, 0, 99),
                 '-v'          : (variant, 1, 1),
                 '--variant'   : (variant, 1, 1),
                 '-q'          : (query, 0, 99),
                 '--query'     : (query, 0, 99),
                 '-D'          : (dry, 0, 0),
                 '--dry'       : (dry, 0, 0)}

    # TODO: This is a bit hacky, and could've been done in a single loop.  Try
    #       to refactor the argument handling part, and at the same time move
    #       the global states into a class, and make the callbacks methods
    argv = {}
    flag = None
    params = None
    for arg in ARGV:
        if arg.startswith('-'):
            argv[arg] = params = []
        else:
            try:
                params.append(arg)
            except AttributeError:
                print(f'Invalid flag: {error}. Try --help', file=stderr)
                exit(1)

    actions = {}
    try:
        for arg, passed_arguments in argv.items():
            callback, argument_count, order = callbacks[arg]
            arguments = []
            for _, argument in zip_longest(range(argument_count),
                                           passed_arguments, fillvalue=None):
                arguments.append(argument)
            actions[callback] = order, arguments
    except KeyError as error:
        print(f'Invalid flag: {error}. Try --help', file=stderr)
        exit(1)

    for action, (_, arguments) in sorted(actions.items(),
                                         key=lambda i: i[1][0]):
        if action(*arguments):
            break
