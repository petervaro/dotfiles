## INFO ##
## INFO ##

from os.path    import expanduser, join
from re         import search, I
from subprocess import run, PIPE

version = run(['blender', '--version'], stdout=PIPE).stdout.split(b'\n')[0]
version = search(rb'blender\s+(\d+\.\d+)', version, I).group(1).decode('utf-8')
path    = expanduser('~/.config/blender')
run(['ln', '-srfn', join(path, version), join(path, 'latest')])
