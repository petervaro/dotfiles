## INFO ##
## INFO ##

from time       import sleep
from itertools  import chain
from subprocess import run, PIPE
from re         import compile, sub


#------------------------------------------------------------------------------#
def pacman():
    result = run('checkupdates', stdout=PIPE, stderr=PIPE, shell=True)
    for info in result.stdout.decode('utf-8').split('\n'):
        if info:
            name, cur_version, _, new_version = info.split()
            yield name, cur_version, new_version



#------------------------------------------------------------------------------#
def pacaur(PATTERN=compile(r'\x1b.+?m')):
    result = run('pacaur -k', stdout=PIPE, stderr=PIPE, shell=True)
    for info in sub(PATTERN, '', result.stdout.decode('utf-8')).split('\n'):
        if info:
            _, _, name, cur_version, _, new_version = info.split()
            yield name, cur_version, new_version



#------------------------------------------------------------------------------#
if __name__ == '__main__':
    try:
        PACKAGE = '  \033[34m* \033[37m{} {} -> {}\033[0m'
        while True:
            print('\033c\033[1;32m==> \033[37m'
                  'The following updates are available:\033[0m')
            i = 0
            for i, info in enumerate(sorted(chain(pacman(), pacaur())), start=1):
                print(PACKAGE.format(*info))
            if i:
                print('\033[1;32m==> \033[37m'
                      'Number of updates available: \033[33m',
                      i, '\033[0m', sep='')
            else:
                print('\033[1;32m==> \033[37mNo updates available\033[0m')
            sleep(300)
    except KeyboardInterrupt:
        print('\n')

