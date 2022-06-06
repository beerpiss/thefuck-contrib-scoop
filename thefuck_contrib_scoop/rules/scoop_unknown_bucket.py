from thefuck.specific.sudo import sudo_support
from thefuck.utils import for_app, get_close_matches, replace_command

from thefuck_contrib_scoop.scoop import get_added_buckets, get_known_buckets


@sudo_support
@for_app("scoop", at_least=3)
def match(command):
    return "scoop bucket" in command.script and (
        "Unknown bucket" in command.output or "bucket not found" in command.output
    )


@sudo_support
def get_new_command(command):
    broken = command.script_parts[3]
    if command.script_parts[2] == "add":
        fix = get_close_matches(broken, get_known_buckets())
        return replace_command(command, broken, fix)
    elif command.script_parts[2] == "rm":
        fix = get_close_matches(broken, get_added_buckets())
        return replace_command(command, broken, fix)
