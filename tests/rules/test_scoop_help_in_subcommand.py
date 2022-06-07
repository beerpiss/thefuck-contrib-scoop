import pytest
from thefuck.types import Command

from thefuck_contrib_scoop.rules.scoop_help_in_subcommand import get_new_command, match


@pytest.mark.parametrize(
    "script",
    [("scoop bucket add --help"), ("scoop alias rm --help")],
)
def test_match(script):
    assert match(Command(script, ""))


@pytest.mark.parametrize(
    "script",
    [
        ("scoop bucket --help"),
        ("scoop alias --help"),
        ("scoop update *"),
        ("scoop"),
        ("adb"),
    ],
)
def test_not_match(script):
    assert not match(Command(script, ""))


@pytest.mark.parametrize(
    "script, new_command",
    [("scoop bucket add --help", "scoop bucket --help")],
)
def test_get_new_command(script, new_command):
    command = Command(script, "")
    assert get_new_command(command) == new_command
