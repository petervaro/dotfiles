## INFO ##
## INFO ##

from datetime   import datetime
from itertools  import islice
from json       import load
from os         import listdir
from os.path    import join, expanduser, isfile
from subprocess import run
from sys        import argv, exit, stderr

SYNC_PATH   = expanduser('~/.package_sync')
DATE_FORMAT = '%Y-%m-%d-%H-%M-%S'
HEAD_NAME   = '__HEAD__'

argv = iter(islice(argv, 1, None))

#------------------------------------------------------------------------------#
def _execute_transaction(transaction_json, transaction_name):
    for transaction in transaction_json[transaction_name]:
        command = transaction['command']
        parameters = transaction.get('parameters', [])
        if isinstance(parameters, str):
            parameters = transaction_json['references'][parameters]
        run(command + parameters)


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

    -i, --initialise
        Sets HEAD to the oldest in the transaction directory.

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

    -u, --upgrade
        Executes all files created after the current HEAD.

    -d, --downgrade [step]
        Executes step number of files before the current HEAD.  If step is not
        given it defaults to 1.  Step can be a negative number for convenience.

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
def init():
    """
    Set HEAD to the oldest file if it hasm't been yet set
    """
    if not isfile(join(SYNC_PATH, HEAD_NAME)):
        with open(join(SYNC_PATH, HEAD_NAME), 'w') as head:
            head.write(_sorted_file_names(reverse=False)[0])


#------------------------------------------------------------------------------#
def new():
    """
    Create a new transaction file
    """
    try:
        editor = next(argv)
    except StopIteration:
        print('Missing positional argument: editor', file=stderr)
        exit(1)
    file_name = f"{datetime.now().strftime(DATE_FORMAT)}.json"
    run((editor, join(SYNC_PATH, file_name)))


#------------------------------------------------------------------------------#
def last():
    """
    Open last transaction file
    """
    try:
        editor = next(argv)
    except StopIteration:
        editor = 'cat'

    file_names = _sorted_file_names(reverse=True)
    if not file_names:
        print('No transaction file found in: {SYNC_PATH}')
        exit(0)

    run((editor, join(SYNC_PATH, file_names[0])))


#------------------------------------------------------------------------------#
def set_():
    """
    Set head to given file without executing any transactions
    """
    try:
        file_name = next(argv)
    except StopIteration:
        print('Missing positional argument: file name', file=stderr)
        exit(1)

    if not isfile(join(SYNC_PATH, file_name)):
        print(f'Not a file: {join(SYNC_PATH, file_name)}', file=stderr)
        exit(1)

    with open(join(SYNC_PATH, HEAD_NAME), 'w') as head:
        head.write(file_name)


#------------------------------------------------------------------------------#
def query():
    """
    List all transaction from oldest to youngest
    """
    with open(join(SYNC_PATH, HEAD_NAME)) as head:
        head_file = head.read()

        for file_name in _sorted_file_names(reverse=False):
            print(file_name,
                  end=' [HEAD]\n' if file_name == head_file else '\n')


#------------------------------------------------------------------------------#
def upgrade():
    """
    Execute all transactions since the current HEAD
    """
    with open(join(SYNC_PATH, HEAD_NAME), 'r+') as head:
        file_name = head_file = head.read()

        execute_transaction = False
        for file_name in _sorted_file_names(reverse=False):
            if execute_transaction:
                with open(join(SYNC_PATH, file_name)) as json:
                    _execute_transaction(load(json), 'upgrade')
            elif file_name == head_file:
                execute_transaction = True

        head.seek(0)
        head.write(file_name)
        head.truncate()


#------------------------------------------------------------------------------#
def downgrade():
    """
    Execute n transactions before the current HEAD
    """
    with open(join(SYNC_PATH, HEAD_NAME), 'r+') as head:
        file_name = head_file = head.read()

        try:
            counter = abs(int(next(argv)))
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

        head.seek(0)
        head.write(file_name)
        head.truncate()


#------------------------------------------------------------------------------#
if __name__ == '__main__':
    try:
        {'-h'          : help,
         '-help'       : help,
         '--help'      : help,
         'help'        : help,
         '-i'          : init,
         '--initialise': init,
         '-n'          : new,
         '--new'       : new,
         '-s'          : set_,
         '--set'       : set_,
         '-l'          : last,
         '--last'      : last,
         '-u'          : upgrade,
         '--upgrade'   : upgrade,
         '-d'          : downgrade,
         '--downgrade' : downgrade,
         '-q'          : query,
         '--query'     : query}[next(argv)]()
    except KeyError:
        print('Invalid sub-command. Try --help', file=stderr)
        exit(1)
    except StopIteration:
        exit(0)
