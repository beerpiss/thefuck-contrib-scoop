import pytest
from thefuck.types import Command

from thefuck_contrib_scoop.rules.scoop_unknown_bucket import get_new_command, match


@pytest.mark.parametrize(
    "script, output",
    [
        (
            "scoop bucket add version",
            "Unknown bucket 'version'. Try specifying <repo>.\n"
            "usage: scoop bucket add <name> [<repo>]",
        ),
    ],
)
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize(
    "script",
    [("scoop bucket list"), ("scoop bucket known")],
)
def test_not_match(script):
    assert not match(Command(script, ""))


@pytest.mark.parametrize(
    "script, output, new_command",
    [
        (
            "scoop bucket add version",
            "Unknown bucket 'version'. Try specifying <repo>.\n"
            "usage: scoop bucket add <name> [<repo>]",
            ["scoop bucket add versions"],
        ),
    ],
)
def test_get_new_command(script, output, new_command):
    command = Command(script, output)
    assert get_new_command(command) == new_command
