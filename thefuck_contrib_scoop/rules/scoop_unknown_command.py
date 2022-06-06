import os
import re

from thefuck.specific.sudo import sudo_support
from thefuck.utils import for_app, replace_command

from thefuck_contrib_scoop.scoop import (
    get_scoop_config,
    get_scoop_prefix,
    scoop_available,
)


@sudo_support
@for_app("scoop")
def match(command):
    return "isn't a scoop command" in command.output.lower()


def _get_commands():
    scoop_libexec = os.path.join(
        get_scoop_prefix(),
        "libexec",
    )
    return list(
        map(
            lambda val: val[:-4][
                6:
            ],  # remove the ".ps1" extension and the "scoop-" prefix
            os.listdir(scoop_libexec),
        )
    )


def _get_aliases():
    return list(get_scoop_config("alias").keys())


@sudo_support
def get_new_command(command):
    misspelled_command = re.compile(r"'(.*)' isn't a scoop command.").findall(
        command.output
    )[0]
    return replace_command(
        command, misspelled_command, _get_commands() + _get_aliases()
    )


enable_by_default = scoop_available
