from thefuck.specific.sudo import sudo_support
from thefuck.utils import for_app

from thefuck_contrib_scoop.scoop import scoop_available


@sudo_support
@for_app("scoop", at_least=2)
def match(command):
    return (
        "scoop install" in command.script and "is already installed" in command.output
    )


@sudo_support
def get_new_command(command):
    return command.script.replace("install", "update")


enable_by_default = scoop_available
