import os
import json
from pathlib import Path


PACKAGE_PATH = Path(__file__).parent.parent.absolute()
DEPLOY_DIR = os.path.join(PACKAGE_PATH, "config", "deploy")
SECRET_FPATH = os.path.join(os.path.join(DEPLOY_DIR, "secret.json"))
CONFIG_FPATH = os.path.join(os.path.join(DEPLOY_DIR, "config.json"))


if os.path.exists(SECRET_FPATH):
    with open(SECRET_FPATH, "r") as f:
        SECRET_DATA = json.load(f)
else:
    SECRET_DATA = dict()


if os.path.exists(CONFIG_FPATH):
    with open(CONFIG_FPATH, "r") as f:
        CONFIG_DATA = json.load(f)
else:
    CONFIG_DATA = dict()


def get_secret_value(key, na_str=""):
    return SECRET_DATA.get(key, na_str)


def get_config_value(key, na_str=""):
    return CONFIG_DATA.get(key, na_str)
