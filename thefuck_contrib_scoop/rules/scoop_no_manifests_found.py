import re
from difflib import get_close_matches

from thefuck.specific.sudo import sudo_support
from thefuck.utils import for_app, get_closest, replace_command

from thefuck_contrib_scoop.scoop import get_manifests, scoop_available

regex = re.compile(
    r"(?:Couldn't|Could not) find manifest for '(.*)'", flags=re.MULTILINE
)


@sudo_support
@for_app("scoop", at_least=2)
def match(command):
    if regex.match(command.output):
        manifest = regex.findall(command.output)[0]
        return bool(get_closest(manifest, get_manifests()))
    return False


@sudo_support
def get_new_command(command):
    broken = regex.findall(command.output)[0]
    return replace_command(
        command, broken, get_close_matches(broken, get_manifests(), cutoff=0.7)
    )


enable_by_default = scoop_available
