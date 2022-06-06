from thefuck.utils import for_app, which

from thefuck_contrib_scoop.scoop import scoop_available


@for_app("scoop", at_least=2)
def match(command):
    return "admin rights" in command.output and (
        "install" in command.script or "uninstall" in command.script
    )


def get_new_command(command):
    if bool(which("sudo")):
        return f"sudo {command.script}"
    else:
        return f'Start-Process -Verb runAs "powershell" "{command.script}"'


enable_by_default = scoop_available
