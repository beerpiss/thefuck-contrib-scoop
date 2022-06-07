import pytest
from thefuck.types import Command

from thefuck_contrib_scoop.rules.scoop_app_isnt_installed import get_new_command, match


@pytest.mark.parametrize(
    "script, output",
    [
        (
            "scoop update gi",
            "ERROR: 'gi' isn't installed.",
        ),
        (
            "scoop reset gi",
            "ERROR 'gi' isn't installed",
        ),
        (
            "scoop prefix gi",
            "Could not find app path for 'gi'",
        ),
        ("scoop hold gi", "ERROR 'gi' is not installed."),
    ],
)
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize(
    "script, output",
    [
        ("scoop depends gi", "Couldn't find manifest for 'gi'."),
        ("scoop info gi", "Could not find manifest for 'gi' in local buckets."),
        ("scoop hold git", "git is now held and can not be updated anymore."),
        ("scoop hlod git", "scoop: 'hlod' isn't a scoop command. See 'scoop help'."),
        (
            "scpop hold git",
            "scpop: The term 'scpop' is not recognized as a name of a cmdlet, function, script file, or executable program.",
        ),
    ],
)
def test_not_match(script, output):
    assert not match(Command(script, output))


@pytest.mark.parametrize(
    "script, output, new_command",
    [
        ("scoop update gi", "ERROR: 'gi' isn't installed.", "scoop update git"),
        ("scoop reset gi", "ERROR 'gi' isn't installed", "scoop reset git"),
        (
            "scoop prefix gi",
            "Could not find app path for 'gi'",
            "scoop prefix git",
        ),
        ("scoop hold gi", "ERROR 'gi' is not installed.", "scoop hold git"),
    ],
)
def test_get_new_command(script, output, new_command):
    assert get_new_command(Command(script, output)) == new_command
