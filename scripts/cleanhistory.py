## INFO ##
## INFO ##

from subprocess import run
from os.path    import expanduser

EXCLUDE  = ('cd',
            'chmod',
            'clear',
            'reset',
            'hh',
            'reboot',
            'poweroff',
            'shutdown',
            'source',
            'ls',
            'startx',
            'mv',
            'rm',
            'cp',
            'cat',
            'echo',
            'printf',
            'cloc',
            'man',
            'mkdir',
            'touch',
            'pass edit',
            'pass generate',
            'git',
            'adb',
            'cini',
            'bash',
            'convert',
            'curl',
            'diff',
            'flask',
            'firefox',
            'grip',
            'nano',
            'mc',
            'mplayer',
            'peerflix',
            'ping',
            'wget',
            'youtube-dl',
            './')
EXCLUDE += tuple('sudo {}'.format(cmd) for cmd in EXCLUDE)

history = set()
with open(expanduser('~/.bash_history'), 'r+') as file:
    for line in file:
        line = line.strip()
        if not line:
            continue
        for exclude in EXCLUDE:
            # TODO: Replace this WIP check with a proper regex
            if (line.lower().startswith(exclude) or
                line.lower().startswith('sudo ' + exclude)):
                break
        else:
            history.add(line)
    file.seek(0)
    file.write('\n'.join(sorted(history)))
    file.truncate()

# Clear history from memory
run('history -c', shell=True)
# Read history from file
run('history -r', shell=True)
# Write file back from memory
run('history -w', shell=True)
