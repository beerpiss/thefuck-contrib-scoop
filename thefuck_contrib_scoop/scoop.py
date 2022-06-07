import itertools
import json
import os
from typing import Union

from thefuck.utils import memoize


def match(_):
    return False


def get_new_command(command):
    return command.script


@memoize
def get_dir():
    return os.getenv("SCOOP") or os.path.join(os.path.expanduser("~"), "scoop")


@memoize
def get_prefix(app="scoop"):
    return os.path.join(get_dir(), "apps", app, "current")


@memoize
def get_config(key):
    scoop_config_file = os.path.join(
        os.path.expanduser("~"), ".config", "scoop", "config.json"
    )
    with open(scoop_config_file, "r") as f:
        scoop_config = json.loads(f.read())
    return scoop_config[key] if key else scoop_config


def get_manifests():
    try:
        buckets_dir = os.path.join(get_dir(), "buckets")
        for bucket in [os.path.join(buckets_dir, x) for x in os.listdir(buckets_dir)]:
            manifest_path = bucket
            if os.path.exists(os.path.join(bucket, "bucket")):
                manifest_path = os.path.join(bucket, "bucket")
            for file in os.listdir(manifest_path):
                if file.endswith(".json"):
                    yield file[:-5]
    except Exception:
        pass


@memoize
def get_added_buckets():
    try:
        buckets_dir = os.path.join(get_dir(), "buckets")
        return os.listdir(buckets_dir)
    except Exception:
        pass


@memoize
def get_known_buckets():
    buckets_json = os.path.join(get_prefix(), "buckets.json")
    with open(buckets_json, "r") as f:
        return list(json.loads(f.read()).keys())


@memoize
def get_installed_apps():
    return os.listdir(os.path.join(get_dir(), "apps"))


@memoize
def get_commands():
    scoop_libexec = os.path.join(
        get_prefix(),
        "libexec",
    )
    return [x[:-4][6:] for x in os.listdir(scoop_libexec)]


@memoize
def get_aliases():
    return list(get_config("alias").keys())


@memoize
def get_help_message(command: str) -> Union["list[str]", None]:
    exec_path = ""
    if command in get_commands():
        exec_path = os.path.join(get_prefix(), "libexec", f"scoop-{command}.ps1")
    elif command in get_aliases():
        exec_path = os.path.join(get_dir(), "shims", f"scoop-{command}.ps1")
    else:
        return None

    help_message_arr = []
    with open(exec_path, "r") as f:
        for line in f:
            if line.startswith("#"):
                help_message_arr.append(line[1:].strip())
            else:
                break
    return help_message_arr


@memoize
def get_available_options(command):
    help_msg = get_help_message(command)
    if help_msg and "Options:" in help_msg:
        options_list = help_msg[help_msg.index("Options:") + 1 :]
        return list(
            itertools.chain.from_iterable(
                [
                    [z.strip().split()[0] for z in y.split(", ")][0:2]
                    for y in options_list
                ]
            )
        )
    else:
        return []


scoop_available = os.path.exists(os.path.join(get_prefix(), "bin", "scoop.ps1"))
