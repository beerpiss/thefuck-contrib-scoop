import pytest
from thefuck.types import Command

from thefuck_contrib_scoop.rules.scoop_config_remove import get_new_command, match


@pytest.mark.parametrize(
    "script",
    [("scoop config remove key")],
)
def test_match(script):
    assert match(Command(script, ""))


@pytest.mark.parametrize(
    "script",
    [
        ("scoop config rm key"),
        ("scoop config key value"),
        ("scoop update *"),
        ("scoop"),
        ("adb"),
    ],
)
def test_not_match(script):
    assert not match(Command(script, ""))


@pytest.mark.parametrize(
    "script, new_command",
    [("scoop config remove key", "scoop config rm remove && scoop config rm key")],
)
def test_get_new_command(script, new_command):
    assert get_new_command(Command(script, "")) == new_command
