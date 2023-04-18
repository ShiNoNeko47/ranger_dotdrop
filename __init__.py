#! /usr/bin/env python3

import os
import yaml
import ranger.api
from ranger.core.linemode import LinemodeBase

CHECKMARK = "  ✔"
DOTDROP_CONFIG = os.getenv("DOTDROP_CONFIG", "")


if DOTDROP_CONFIG:
    with open(DOTDROP_CONFIG) as config:
        config = yaml.safe_load(config)

files = [
    os.path.expanduser(config["dotfiles"][file]["dst"]) for file in config["dotfiles"]
]


@ranger.api.register_linemode
class LinemodeDotdrot(LinemodeBase):
    name = "dotdrop"
    uses_metadata = False

    def filetitle(self, file, metadata):
        return file.relative_path + file_included(file.path, CHECKMARK)


def file_included(file, checkmark):
    if DOTDROP_CONFIG == "" or file == "/":
        return ""

    if file in files:
        return checkmark

    return file_included(os.path.dirname(file), checkmark)
