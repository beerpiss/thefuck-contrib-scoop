import pytest
from thefuck.types import Command

from thefuck_contrib_scoop.rules.scoop_admin_global_apps import get_new_command, match


@pytest.mark.parametrize(
    "script, output",
    [
        (
            "scoop install -g itunes-np",
            "ERROR: you need admin rights to install global apps",
        ),
        (
            "scoop update -g itunes-np",
            "ERROR: You need admin rights to update global apps.",
        ),
        (
            "scoop uninstall -g itunes-np",
            "ERROR You need admin rights to uninstall global apps.",
        ),
        (
            "scoop cleanup -g itunes-np",
            "ERROR: you need admin rights to cleanup global apps",
        ),
    ],
)
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize(
    "script",
    [
        ("scoop update *"),
        ("scoop update python"),
        ("scoop install python"),
        ("scoop cleanup python"),
        ("scoop uninstall python"),
        ("scoop"),
        ("scopo"),
    ],
)
def test_not_match(script):
    assert not match(Command(script, ""))


@pytest.mark.parametrize(
    "script, output, new_command, sudo_available",
    [
        (
            f"scoop {action} -g itunes-np",
            f"ERROR: you need admin rights to {action} global apps",
            f"sudo scoop {action} -g itunes-np",
            bool(True),
        )
        for action in ["install", "cleanup"]
    ]
    + [
        (
            f"scoop {action} -g itunes-np",
            f"ERROR: you need admin rights to {action} global apps",
            f'Start-Process -Verb runAs "powershell" "scoop {action} -g itunes-np"',
            False,
        )
        for action in ["install", "cleanup"]
    ]
    + [
        (
            "scoop update -g itunes-np",
            "ERROR: You need admin rights to update global apps.",
            "sudo scoop update -g itunes-np",
            True,
        ),
        (
            "scoop uninstall -g itunes-np",
            "ERROR You need admin rights to uninstall global apps.",
            "sudo scoop uninstall -g itunes-np",
            True,
        ),
    ]
    + [
        (
            "scoop update -g itunes-np",
            "ERROR: You need admin rights to update global apps.",
            'Start-Process -Verb runAs "powershell" "scoop update -g itunes-np"',
            False,
        ),
        (
            "scoop uninstall -g itunes-np",
            "ERROR You need admin rights to uninstall global apps.",
            'Start-Process -Verb runAs "powershell" "scoop uninstall -g itunes-np"',
            False,
        ),
    ],
)
def test_get_new_command(script, output, new_command, sudo_available):
    assert (
        get_new_command(Command(script, output), sudo_available=sudo_available)
        == new_command
    )
