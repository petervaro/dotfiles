## INFO ##
## INFO ##

from re         import search, finditer, compile, MULTILINE, VERBOSE, DOTALL
from subprocess import run, PIPE
from sys        import argv, exit

_, *arguments = argv

if not arguments:
    exit(0)

focus_off = arguments[0] in ('-o', '--off')

# Get all connnected monitors
command = 'xrandr', '--current'
pattern = compile(br"""
    ^(?P<name>.+)
    \s+connected\s+(?:primary\s+)?
    (?P<width>\d+)
    x
    (?P<height>\d+)
    \+
    (?P<x>\d+)
    \+
    (?P<y>\d+)""", MULTILINE | VERBOSE)
monitors = [
    {'name'  : m['name'],
     'width' : int(m['width']),
     'height': int(m['height']),
     'x'     : int(m['x']),
     'y'     : int(m['width'])} for m in finditer(pattern,
                                                  run(command,
                                                      stdout=PIPE).stdout)]

def adjust_brightness(output, level):
    run(('xrandr', '--output', output, '--brightness', level))

if focus_off:
    for monitor in monitors:
        adjust_brightness(monitor['name'], '1.0')
    exit(0)

# Get currently active window ID
command = 'xdotool', 'getactivewindow'
window = run(command, stdout=PIPE).stdout

# Get properties of the currently active window
command = 'xwininfo', '-id', window
pattern = compile(br"""
    Absolute\s+upper-left\s+X:\s*(?P<x>\d+)
    .*?
    Absolute\s+upper-left\s+Y:\s*(?P<y>\d+)
    .*?
    Width:\s*(?P<width>\d+)
    .*?
    Height:\s*(?P<height>\d+)""", MULTILINE | VERBOSE | DOTALL)
match = search(pattern, run(command, stdout=PIPE).stdout)
window = {'width' : int(match['width']),
          'height': int(match['height']),
          'x'     : int(match['x']),
          'y'     : int(match['y'])}

# Decide which monitor has the currently active window
# TODO: This bound checking is currently only working for horizontal alignments,
#       but should be easily be converted into a universal one at some point
unfocused_monitor_names = []
monitor_found = False
for monitor in monitors:
    # If monitor containing the window not yet found
    if not monitor_found:
        wx = window['x']
        ww = window['width']
        mx = monitor['x']
        mw = monitor['width']
        # If window is fully or bigger area of it is on this monitor
        if ((mx <= wx <= mx + mw and       # top-left corner is on this monitor
             (mx <= wx + ww <= mx + mw or  # top-right corner is on this monitor
              mx + mw - wx > ww//2) or     # bigger area is on this monitor
            (mx <= wx + ww <= mx + mw and  # top-right corner on this monitor
             mx - wx < ww//2))):           # bigger area is on this monitor
                monitor_found = True
                continue

    # Collect unfocused monitors
    unfocused_monitor_names.append(monitor['name'])
    # Adjust brightness of all the other monitors
    adjust_brightness(monitor['name'], '0.2')

# Run passed commands
run(arguments)

# Reset brightness back to normal
for monitor_name in unfocused_monitor_names:
    adjust_brightness(monitor_name, '1.0')
