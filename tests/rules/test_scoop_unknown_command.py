import pytest
from thefuck.types import Command

from thefuck_contrib_scoop.rules.scoop_unknown_command import get_new_command, match
from thefuck_contrib_scoop.scoop import get_aliases, get_commands


@pytest.mark.parametrize(
    "script, output",
    [
        (
            "scoop bucke add versions",
            "scoop: 'bucke' isn't a scoop command. See 'scoop help'.",
        ),
    ],
)
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize(
    "script",
    [(f"scoop {command}") for command in get_commands() + get_aliases()],
)
def test_not_match(script):
    assert not match(Command(script, ""))


@pytest.mark.parametrize(
    "script, output, new_command",
    [
        (
            "scoop inst thefuck",
            "scoop: 'inst' isn't a scoop command. See 'scoop help'.",
            [
                "scoop install thefuck",
                "scoop uninstall thefuck",
                "scoop list thefuck",
            ],
        ),
        (
            "scoop instaa thefuck",
            "scoop: 'instaa' isn't a scoop command. See 'scoop help'.",
            [
                "scoop install thefuck",
                "scoop uninstall thefuck",
                "scoop list thefuck",
            ],
        ),
    ],
)
def test_get_new_command(script, output, new_command):
    command = Command(script, output)
    assert sorted(get_new_command(command)) == sorted(new_command)
