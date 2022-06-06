from thefuck.utils import for_app

from thefuck_contrib_scoop.scoop import scoop_available


@for_app("scoop", at_least=3)
def match(command):
    return "scoop config remove" in command.script


def get_new_command(command):
    return f"scoop config rm remove && scoop config rm {command.script_parts[-1]}"


enable_by_default = scoop_available
