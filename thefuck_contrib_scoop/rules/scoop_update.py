from thefuck.specific.sudo import sudo_support
from thefuck.types import Command
from thefuck.utils import for_app


@sudo_support
@for_app("scoop", at_least=1)
def match(command: Command) -> bool:
    return "update" in command.script_parts[1] and len(command.script_parts) == 2


@sudo_support
def get_new_command(_: Command) -> str:
    return "scoop update *"
