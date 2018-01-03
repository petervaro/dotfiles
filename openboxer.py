## INFO ##
## INFO ##

from json            import load
from sys             import argv, exit, stderr
from xml.dom.minidom import parseString as parse_xml

try:
    VARIANT = argv[1]
except IndexError:
    print('Missing argument: variant', file=stderr)
    exit(1)

def with_main_key(function):
    def wrapper(config, *args, **kwargs):
        result = []
        for main_key in config['main_keys']:
            result.append(function(config, main_key, *args, **kwargs))
        return ''.join(result)
    return wrapper

def keyboard_action(_, main_key='', key='', action='', **action_options):
    main_key = main_key and f'{main_key}-'
    if action_options:
        action = [f'<action name="{action}">']
        for option, value in action_options.items():
            action.append(f'<{option}>{value}</{option}>')
        action.append('</action>')
        action = ''.join(action)
    else:
        action = f'<action name="{action}"/>'
    return (f'<keybind key="{main_key}{key}">'
                f'{action}'
            '</keybind>')

@with_main_key
def keyboard_move_resize(config, main_key):
    keybinds = []
    for open_key, key_chains in config['screen_key_chains'].items():
        actions = []
        for close_key, (matrix, *range) in key_chains.items():
            matrix = config['screen_matrices'][matrix]
            start = matrix[range[0]]
            try:
                stop = matrix[range[1]]
                x = min(start['x'], stop['x'])
                y = min(start['y'], stop['y'])
                if start['x'] == stop['x']:
                    width = start['width']
                else:
                    width = (max(start['x'], stop['x']) -
                             min(start['x'], stop['x']) +
                             min(start['width'], stop['width']))
                if start['y'] == stop['y']:
                    height = start['height']
                else:
                    height = (max(start['y'], stop['y']) -
                              min(start['y'], stop['y']) +
                              min(start['height'], stop['height']))
            except IndexError:
                x      = start['x']
                y      = start['y']
                width  = start['width']
                height = start['height']
            actions.append(f'<keybind key="{close_key}">'
                                '<action name="UnmaximizeFull"/>'
                                '<action name="MoveResizeTo">'
                                    f'<x>{x}</x>'
                                    f'<y>{y}</y>'
                                    f'<width>{width}</width>'
                                    f'<height>{height}</height>'
                                '</action>'
                            '</keybind>')
        keybinds.append(f'<keybind key="{main_key}-{open_key}">'
                             f"{''.join(actions)}"
                        '</keybind>')
    return ''.join(keybinds)

@with_main_key
def keyboard_window_switch(_, main_key, key, action, all_desktops):
    all_desktops = 'yes' if all_desktops else 'no'
    return (f'<keybind key="{main_key}-{key}">'
                f'<action name="{action}">'
                    f'<allDesktops>{all_desktops}</allDesktops>'
                    '<dialog>list</dialog>'
                    '<bar>yes</bar>'
                    '<raise>yes</raise>'
                    '<finalactions>'
                        '<action name="Focus"/>'
                        '<action name="Raise"/>'
                        '<action name="Unshade"/>'
                    '</finalactions>'
                '</action>'
            '</keybind>')

@with_main_key
def keyboard_monitor_toggle(_, main_key, key):
    return (f'<keybind key="{main_key}-{key}">'
                '<action name="If">'
                    '<query target="focus">'
                        '<monitor>1</monitor>'
                    '</query>'
                    '<then>'
                        '<action name="MoveResizeTo">'
                            '<monitor>2</monitor>'
                        '</action>'
                    '</then>'
                    '<else>'
                        '<action name="MoveResizeTo">'
                            '<monitor>1</monitor>'
                        '</action>'
                    '</else>'
                '</action>'
            '</keybind>')

#--- CONSTRUCT ----------------------------------------------------------------#

KEYBOARD = ((with_main_key(keyboard_action),
                # Navigate between desktops (arrow keys)
                {'action': 'GoToDesktop',
                 'key'   : 'Left',
                 'to'    : 'left',
                 'wrap'  : 'yes'},
                {'action': 'GoToDesktop',
                 'key'   : 'Right',
                 'to'    : 'right',
                 'wrap'  : 'yes'},
                # Send windows between desktops
                {'action': 'SendToDesktop',
                 'key'   : 'S-Left',
                 'to'    : 'left',
                 'wrap'  : 'yes',
                 'follow': 'no'},
                {'action': 'SendToDesktop',
                 'key'   : 'S-Right',
                 'to'    : 'right',
                 'wrap'  : 'yes',
                 'follow': 'no'},
                # Navigate between desktops (function keys)
                *tuple({'action': 'GoToDesktop',
                        'key'   : f'F{i}',
                        'to'    : i} for i in range(1, 13)),
                *tuple({'action': 'SendToDesktop',
                        'key'   : f'S-F{i}',
                        'follow': 'no',
                        'to'    : i} for i in range(1, 13)),
                # Manage desktops
                {'action': 'AddDesktop',
                 'key'   : 'Insert',
                 'where' : 'last'},
                {'action': 'RemoveDesktop',
                 'key'   : 'Delete',
                 'where' : 'last'},
                # Hide all
                {'action': 'ToggleShowDesktop',
                 'key'   : 'BackSpace'}),
            (keyboard_move_resize, {}),
            (with_main_key(keyboard_action),
                # Title bar actions
                {'action': 'ToggleMaximize',
                 'key'   : 'KP_Add'},
                {'action': 'ToggleFullscreen',
                 'key'   : 'KP_Subtract'},
                {'action': 'Close',
                 'key'   : 'W'},
                {'action': 'ShowMenu',
                 'key'   : 'space',
                 'menu'  : 'client-menu'}),
            (keyboard_window_switch, {'action'      : 'NextWindow',
                                      'key'         : 'Tab',
                                      'all_desktops': True},
                                     {'action'      : 'NextWindow',
                                      'key'         : 'Down',
                                      'all_desktops': True},
                                     {'action'      : 'NextWindow',
                                      'key'         : 'C-Tab',
                                      'all_desktops': False},
                                     {'action'      : 'NextWindow',
                                      'key'         : 'C-Down',
                                      'all_desktops': False},
                                     {'action'      : 'PreviousWindow',
                                      'key'         : 'S-Tab',
                                      'all_desktops': True},
                                     {'action'      : 'PreviousWindow',
                                      'key'         : 'Up',
                                      'all_desktops': True},
                                     {'action'      : 'PreviousWindow',
                                      'key'         : 'S-C-Tab',
                                      'all_desktops': False},
                                     {'action'      : 'PreviousWindow',
                                      'key'         : 'C-Up',
                                      'all_desktops': False}),
            (keyboard_monitor_toggle, {'key': 'KP_0'}),
            (with_main_key(keyboard_action),
                # Logout
                {'action': 'Exit',
                 'key'   : 'Escape',
                 'prompt': 'yes'},
                # Reload configuration
                {'action': 'Reconfigure',
                 'key'   : 'R'},
                # Application launcher
                {'action' : 'Execute',
                 'key'    : 'Return',
                 'command': 'rofi -show run'},
                # Open terminal
                {'action' : 'Execute',
                 'key'    : 'S-Return',
                 'command': 'urxvt'}),
            (keyboard_action,
                # Pause MOC player
                {'action' : 'Execute',
                 'key'    : 'XF86AudioPlay',
                 'command': 'mocp --toggle-pause'},
                # Stop MOC player
                {'action' : 'Execute',
                 'key'    : 'XF86AudioStop',
                 'command': 'mocp --stop'},
                # Previous track in MOC player
                {'action' : 'Execute',
                 'key'    : 'XF86AudioPrev',
                 'command': 'mocp --previous'},
                # Next track in MOC player
                {'action' : 'Execute',
                 'key'    : 'XF86AudioNext',
                 'command': 'mocp --next'},
                # Mute system
                # TODO: Get current volume and send a notification to dunst
                {'action' : 'Execute',
                 'key'    : 'XF86AudioMute',
                 'command': 'pactl set-sink-mute 0 toggle'},
                # Lower system volume
                # TODO: Get current volume and send a notification to dunst
                {'action' : 'Execute',
                 'key'    : 'XF86AudioLowerVolume',
                 'command': 'pactl set-sink-volume 0 -5%'},
                # Raise system volume
                # TODO: Get current volume and send a notification to dunst
                {'action' : 'Execute',
                 'key'    : 'XF86AudioRaiseVolume',
                 'command': 'pactl set-sink-volume 0 +5%'},
                # Take screenshot
                {'action' : 'Execute',
                 'key'    : 'Print',
                 'command': 'spectacle'},
                # Lock screen
                {'action' : 'Execute',
                 'key'    : 'Scroll_Lock',
                 'command': 'scrlock.sh'},
                # Turn off monitors
                {'action' : 'Execute',
                 'key'    : 'Pause',
                 'command': 'scroff.sh'}))

with open(f'openbox_{VARIANT}/openboxer_rc.json') as json:
    config = load(json)

KEYBINDS = []
diverge  = config.get('diverge', {})
for function, *parameters in KEYBOARD:
    for parameter in parameters:
        action = parameter.get('action')
        if action in diverge:
            parameter.update(diverge[action])
        KEYBINDS.append(function(config, **parameter))

with open(f'openbox_{VARIANT}/rc.xml', 'w') as xml:
    parse_xml((
        '<?xml version="1.0" encoding="UTF-8"?>'

        '<openbox_config xmlns="http://openbox.org/3.4/rc" '
                        'xmlns:xi="http://www.w3.org/2001/XInclude">'

            '<resistance>'
                '<strength>10</strength>'
                '<screen_edge_strength>20</screen_edge_strength>'
            '</resistance>'

            '<focus>'
                '<focusNew>yes</focusNew>'
                '<followMouse>yes</followMouse>'
                '<focusLast>no</focusLast>'
                '<underMouse>no</underMouse>'
                '<focusDelay>500</focusDelay>'
                '<raiseOnFocus>yes</raiseOnFocus>'
            '</focus>'

            '<placement>'
                '<policy>UnderMouse</policy>'
                '<center>yes</center>'
                '<monitor>Mouse</monitor>'
                '<primaryMonitor>Mouse</primaryMonitor>'
            '</placement>'

            '<theme>'
                '<name>Arc</name>'
                '<keepBorder>yes</keepBorder>'
                '<animateIconify>yes</animateIconify>'
            '</theme>'

            '<desktops>'
                '<number>4</number>'
                '<firstdesk>1</firstdesk>'
                '<popupTime>875</popupTime>'
            '</desktops>'

            '<resize>'
                '<drawContents>yes</drawContents>'
                '<popupShow>Nonpixel</popupShow>'
                '<popupPosition>Center</popupPosition>'
            '</resize>'

            '<mouse>'
                '<dragThreshold>1</dragThreshold>'
                '<doubleClickTime>500</doubleClickTime>'
                '<screenEdgeWarpTime>0</screenEdgeWarpTime>'
                '<screenEdgeWarpMouse>false</screenEdgeWarpMouse>'
                '<context name="Frame">'
                    '<mousebind button="W-Left" action="Drag">'
                        '<action name="Focus"/>'
                        '<action name="Raise"/>'
                        '<action name="Move"/>'
                    '</mousebind>'
                    '<mousebind button="W-Right" action="Drag">'
                        '<action name="Focus"/>'
                        '<action name="Raise"/>'
                        '<action name="Resize"/>'
                    '</mousebind>'
                '</context>'
                '<context name="Client">'
                    '<mousebind button="Left" action="Press">'
                        '<action name="Focus"/>'
                        '<action name="Raise"/>'
                    '</mousebind>'
                    '<mousebind button="Right" action="Press">'
                        '<action name="Focus"/>'
                        '<action name="Raise"/>'
                    '</mousebind>'
                '</context>'
            '</mouse>'

            '<applications>'
                '<application name="*">'
                    '<decor>no</decor>'
                    '<focus>yes</focus>'
                '</application>'
            '</applications>'

            '<keyboard>'
                f"{''.join(KEYBINDS)}"
            '</keyboard>'
        '</openbox_config>')).writexml(xml, addindent=' '*4, newl='\n')
