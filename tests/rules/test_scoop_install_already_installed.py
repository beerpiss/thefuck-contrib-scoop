import pytest
from thefuck.types import Command

from thefuck_contrib_scoop.rules.scoop_install_already_installed import (
    get_new_command,
    match,
)


@pytest.mark.parametrize(
    "script, output",
    [
        (
            "scoop install git",
            "WARN  'git' (2.36.1.windows.1) is already installed.\nUse 'scoop update git' to install a new version.",
        )
    ],
)
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize(
    "script",
    [
        ("scoop update git"),
        ("scoop update"),
        ("scoop update *"),
    ],
)
def test_not_match(script):
    assert not match(Command(script, ""))


@pytest.mark.parametrize(
    "script, output, new_command",
    [
        (
            "scoop install git",
            "WARN  'git' (2.36.1.windows.1) is already installed.\nUse 'scoop update git' to install a new version.",
            "scoop update git",
        ),
    ],
)
def test_get_new_command(script, output, new_command):
    command = Command(script, output)
    assert get_new_command(command) == new_command
