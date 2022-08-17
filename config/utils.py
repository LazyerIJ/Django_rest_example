import os
from config.settings import BASE_DIR


DEPLOY_DIR = os.path.join(BASE_DIR, "deploy")
SECRET_FPATH = os.path.join(os.path.join(DEPLOY_DIR, "secret.json"))


if os.path.exists(SECRET_FPATH):
    with open(SECRET_FPATH, "r") as f:
        SECRET_DATA = f.readline()
else:
    SECRET_DATA = dict()


def get_secret_value(key, na_str=""):
    return SECRET_DATA.get(key, na_str)
