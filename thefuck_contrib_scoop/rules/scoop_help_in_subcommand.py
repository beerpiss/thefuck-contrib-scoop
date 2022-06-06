from thefuck.specific.sudo import sudo_support
from thefuck.utils import for_app

from thefuck_contrib_scoop.scoop import scoop_available


@sudo_support
@for_app("scoop", at_least=3)
def match(command):
    return command.script_parts[3] == "--help" or command.script_parts[3] == "-h"


@sudo_support
def get_new_command(command):
    del command._script_parts[2]
    return " ".join(command._script_parts)


enable_by_default = scoop_available
