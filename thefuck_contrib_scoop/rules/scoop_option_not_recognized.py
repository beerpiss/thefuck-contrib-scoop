import re

from thefuck.specific.sudo import sudo_support
from thefuck.utils import for_app, get_closest, replace_argument

from thefuck_contrib_scoop.scoop import get_available_options


@sudo_support
@for_app("scoop")
def match(command):
    return "Option" in command.output and "not recognized" in command.output


@sudo_support
def get_new_command(command):
    broken = re.findall(r"Option ([\-a-z]+) not recognized", command.output)[0]
    return replace_argument(
        command.script,
        broken,
        get_closest(broken, get_available_options(command.script_parts[1])),
    )
