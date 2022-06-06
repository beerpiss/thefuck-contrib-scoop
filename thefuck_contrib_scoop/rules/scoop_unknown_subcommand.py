from thefuck.specific.sudo import sudo_support
from thefuck.utils import for_app, get_close_matches, replace_command

from thefuck_contrib_scoop.scoop import scoop_available


def _match(output):
    return "Usage: scoop" in output and "[<args>]" in output


@sudo_support
@for_app("scoop", at_least=2)
def match(command):
    return _match(command.output)


def _get_subcommands(usage, orig):
    valid_subcommands = next(x for x in usage.split() if "|" in x).split("|")
    return get_close_matches(orig, valid_subcommands)


@sudo_support
def get_new_command(command):
    usage = next(x for x in command.output.splitlines() if _match(x))
    broken = command.script_parts[2]
    if broken == "remove":  # Special case
        return replace_command(command, broken, ["rm"])
    fixes = _get_subcommands(usage, broken)
    return replace_command(command, broken, fixes)


enable_by_default = scoop_available
