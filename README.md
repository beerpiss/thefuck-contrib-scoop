# thefuck-contrib-scoop
[*The Fuck*](https://github.com/nvbn/thefuck) rules for [Scoop](https://github.com/ScoopInstaller/Scoop).

## Installation
[Install *The Fuck*](https://github.com/nvbn/thefuck#installation) if you haven't.

```
pip install git+https://github.com/beerpiss/thefuck-contrib-scoop@trunk
```

## Rules
- `scoop_admin_global_apps`: Elevates permission so `scoop <install/uninstall> --global` can work.
- `scoop_help_in_subcommand`: Subcommands such as `scoop bucket add` don't take a `--help` switch, so this rule removes the subcommand.
- `scoop_install_already_installed`: Turns `scoop install <app>` into `scoop update <app>`
- `scoop_install_no_manifests_found`: Fixes app name for `scoop install`
- `scoop_unknown_bucket`: Fixes bucket name for `scoop bucket add|rm`
- `scoop_unknown_command`: Fixes wrong commands, e.g. `scoop bucke/scoop bucket`
- `scoop_unknown_subcommand`: Fixes wrong subcommands, e.g. `scoop bucket remove/scoop bucket rm`