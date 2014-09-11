__author__ = 'tylar'

import code
import readline
import rlcompleter


def open_console():
    # use this to open the interactive console for debugging
    vars = globals()
    vars.update(locals())
    readline.set_completer(rlcompleter.Completer(vars).complete)
    readline.parse_and_bind("tab: complete")
    shell = code.InteractiveConsole(vars)
    shell.interact()