from thefuck.specific.sudo import sudo_support
from thefuck.utils import for_app


@sudo_support
@for_app("scoop")
def match(command):
    return command.script == "scoop update"


def get_new_command(_):
    return "scoop update *"
