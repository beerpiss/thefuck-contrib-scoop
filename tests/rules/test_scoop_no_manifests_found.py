import pytest
from thefuck.types import Command

from thefuck_contrib_scoop.rules.scoop_no_manifests_found import get_new_command, match


@pytest.mark.parametrize(
    "script, output",
    [
        (
            "scoop install gi",
            "Couldn't find manifest for 'gi'.",
        ),
        (
            "scoop info gi",
            "Could not find manifest for 'gi' in local buckets.",
        ),
    ],
)
def test_match(script, output):
    assert match(Command(script, output))


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
def test_not_match(script, output):
    assert not match(Command(script, output))


@pytest.mark.parametrize(
    "script, output, new_command",
    [
        (
            "scoop install gi",
            "Couldn't find manifest for 'gi'.",
            ["scoop install git"],
        ),
        (
            "scoop info gi",
            "Could not find manifest for 'gi' in local buckets.",
            ["scoop info git"],
        ),
        (
            "scoop install xmind7",
            "Couldn't find manifest for 'xmind7'.",
            ["scoop install xmind", "scoop install xmind8", "scoop install xming"],
        ),
    ],
)
def test_get_new_command(script, output, new_command):
    command = Command(script, output)
    assert get_new_command(command) == new_command
