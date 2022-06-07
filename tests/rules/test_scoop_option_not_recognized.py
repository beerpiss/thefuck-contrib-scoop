import pytest
from thefuck.types import Command

from thefuck_contrib_scoop.rules.scoop_option_not_recognized import (
    get_new_command,
    match,
)


@pytest.mark.parametrize(
    "script, output",
    [
        (
            "scoop install -v git",
            "scoop install: Option -v not recognized.",
        ),
    ],
)
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize(
    "script, output",
    [
        (
            "scoop install --help",
            "Usage: scoop install <app> [options]\n"
            "\n"
            "e.g. The usual way to install an app (uses your local 'buckets'):\n"
            "     scoop install git\n"
            "To install an app from a manifest at a URL:\n"
            "     scoop install https://raw.githubusercontent.com/ScoopInstaller/Main/master/bucket/runat.json\n"
            "To install an app from a manifest on your computer\n"
            "     scoop install \\path\\to\\app.json\n"
            "Options:\n"
            "  -g, --global              Install the app globally\n"
            "  -i, --independent         Don't install dependencies automatically\n"
            "  -k, --no-cache            Don't use the download cache\n"
            "  -u, --no-update-scoop     Don't update Scoop before installing if it's outdated\n"
            "  -s, --skip                Skip hash validation (use with caution!)\n"
            "  -a, --arch <32bit|64bit>  Use the specified architecture, if the app supports it\n",
        ),
    ],
)
def test_not_match(script, output):
    assert not match(Command(script, output))


@pytest.mark.parametrize(
    "script, output, new_command",
    [
        (
            "scoop install -v git",
            "scoop install: Option -v not recognized.",
            "scoop install -g git",
        ),
    ],
)
def test_get_new_command(script, output, new_command):
    command = Command(script, output)
    assert get_new_command(command) == new_command
