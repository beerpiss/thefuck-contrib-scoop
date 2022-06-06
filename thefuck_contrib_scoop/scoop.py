import json
import os

from thefuck.utils import memoize, which

scoop_available = bool(which("scoop"))


def match(_):
    return False


def get_new_command(command):
    return command.script


@memoize
def get_scoop_dir():
    return os.getenv("SCOOP") or os.path.join(os.path.expanduser("~"), "scoop")


@memoize
def get_scoop_prefix():
    return os.path.join(get_scoop_dir(), "apps", "scoop", "current")


@memoize
def get_scoop_config(key):
    scoop_config_file = os.path.join(
        os.path.expanduser("~"), ".config", "scoop", "config.json"
    )
    with open(scoop_config_file, "r") as f:
        scoop_config = json.loads(f.read())
    return scoop_config[key] if key else scoop_config


def get_manifests():
    try:
        buckets_dir = os.path.join(get_scoop_dir(), "buckets")
        for bucket in list(
            map(lambda x: os.path.join(buckets_dir, x), os.listdir(buckets_dir))
        ):
            manifest_path = bucket
            if os.path.exists(os.path.join(bucket, "bucket")):
                manifest_path = os.path.join(bucket, "bucket")
            for file in os.listdir(manifest_path):
                if file.endswith(".json"):
                    yield file[:-5]
    except Exception:
        pass


def get_added_buckets():
    try:
        buckets_dir = os.path.join(get_scoop_dir(), "buckets")
        return os.listdir(buckets_dir)
    except Exception:
        pass


def get_known_buckets():
    buckets_json = os.path.join(get_scoop_prefix(), "buckets.json")
    with open(buckets_json, "r") as f:
        return list(json.loads(f.read()).keys())
