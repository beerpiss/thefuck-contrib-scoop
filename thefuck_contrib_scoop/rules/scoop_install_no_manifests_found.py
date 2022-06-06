import re

from thefuck.specific.sudo import sudo_support
from thefuck.utils import for_app, get_close_matches, replace_command

from thefuck_contrib_scoop.scoop import get_manifests, scoop_available

regex = re.compile(r"Couldn't find manifest for '(.*)'")


def _get_similar_manifest(name):
    return get_close_matches(name, get_manifests(), cutoff=0.7)


@sudo_support
@for_app("scoop", at_least=2)
def match(command):
    is_proper_command = (
        "scoop install" in command.script
        and "Couldn't find manifest for" in command.output
    )

    if is_proper_command:
        manifest = regex.findall(command.output)[0]
        return len(_get_similar_manifest(manifest)) > 0
    return False


@sudo_support
def get_new_command(command):
    not_exist_manifest = regex.findall(command.output)[0]
    exist_manifest = _get_similar_manifest(not_exist_manifest)

    return replace_command(command, not_exist_manifest, exist_manifest)


enable_by_default = scoop_available
