import os
import re

from thefuck.specific.sudo import sudo_support
from thefuck.utils import for_app, replace_command

from thefuck_contrib_scoop.scoop import get_aliases, get_commands, scoop_available


@sudo_support
@for_app("scoop")
def match(command):
    return "isn't a scoop command" in command.output.lower()


@sudo_support
def get_new_command(command):
    misspelled_command = re.compile(r"'(.*)' isn't a scoop command.").findall(
        command.output
    )[0]
    return replace_command(command, misspelled_command, get_commands() + get_aliases())


enable_by_default = scoop_available
