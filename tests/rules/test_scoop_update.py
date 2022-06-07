import pytest
from thefuck.types import Command

from thefuck_contrib_scoop.rules.scoop_update import get_new_command, match


@pytest.mark.parametrize(
    "script",
    [("scoop update")],
)
def test_match(script):
    assert match(Command(script, ""))


@pytest.mark.parametrize(
    "script",
    [("scoop update *"), ("scoop update python")],
)
def test_not_match(script):
    assert not match(Command(script, ""))


@pytest.mark.parametrize("script, new_command", [("scoop update", "scoop update *")])
def test_get_new_command(script, new_command):
    assert get_new_command(Command(script, "")) == new_command
