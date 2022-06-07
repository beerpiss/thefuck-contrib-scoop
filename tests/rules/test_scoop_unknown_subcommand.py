import pytest
from thefuck.types import Command

from thefuck_contrib_scoop.rules.scoop_unknown_subcommand import get_new_command, match


@pytest.mark.parametrize(
    "script, output",
    [
        (
            "scoop bucket ad versions",
            "scoop bucket: cmd 'ad' not supported\n"
            "Usage: scoop bucket add|list|known|rm [<args>]",
        ),
        (
            "scoop bucket remove versions",
            "scoop bucket: cmd 'remove' not supported\n"
            "Usage: scoop bucket add|list|known|rm [<args>]",
        ),
    ],
)
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize(
    "script",
    [("scoop bucket add versions")],
)
def test_not_match(script):
    assert not match(Command(script, ""))


@pytest.mark.parametrize(
    "script, output, new_command",
    [
        (
            "scoop bucket ad versions",
            "scoop bucket: cmd 'ad' not supported\n"
            "Usage: scoop bucket add|list|known|rm [<args>]",
            ["scoop bucket add versions"],
        ),
        (
            "scoop bucket remove versions",
            "scoop bucket: cmd 'remove' not supported\n"
            "Usage: scoop bucket add|list|known|rm [<args>]",
            ["scoop bucket rm versions"],
        ),
    ],
)
def test_get_new_command(script, output, new_command):
    command = Command(script, output)
    assert get_new_command(command) == new_command
