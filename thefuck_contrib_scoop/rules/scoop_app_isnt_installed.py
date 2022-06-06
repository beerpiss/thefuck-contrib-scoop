import re

from thefuck.utils import for_app, get_closest
from thefuck.specific.sudo import sudo_support

from thefuck_contrib_scoop.scoop import get_installed_apps


@sudo_support
@for_app("scoop", at_least=2)
def match(command):
    return "is not installed" in command.output or "isn't installed" in command.output


@sudo_support
def get_new_command(command):
    brokens = re.findall(
        r"'(.*)' (?:isn't|is not) installed", command.output, flags=re.MULTILINE
    )
    ret = command.script
    for broken in brokens:
        fix = get_closest(broken, get_installed_apps())
        ret = ret.replace(broken, fix)
    return ret
