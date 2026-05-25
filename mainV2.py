from math import e
import subprocess
import sys
from typing import NamedTuple
from rich.console import Console
from rich.prompt import Confirm
from pathlib import Path
import os
import argparse

class Args(NamedTuple):
    project_title: str
    language: str
    config: str


PROJECTS_DIR = Path.home() / "projects" / "programming"
PYMPD_CONF = Path.home() / ".config" / "pympd"  
console = Console(color_system="truecolor")


def user_confirm(prompt) -> bool:
    return Confirm().ask(prompt)

def config_dir_exist():
    if not Path(PYMPD_CONF).is_dir():
        Path.mkdir(PYMPD_CONF)


def get_config(language, config) ->None|Path:
    if not config_dir_exist():
        return 
    elif Path(PYMPD_CONF / language / config).is_dir():
        return Path(PYMPD_CONF / language / config)



def get_pre_make_commands(args: Args):
    commands = []
    config_path = get_config(args.language, args.config)
    assert config_path is not None
    commands_file = (config_path / ".commands.txt").absolute().as_posix()
    with open(commands_file, "r") as file:
        f_data = file.readlines()
    for line in f_data:
        if "POST:" in line:
            break
        if "PRE:" in line:
            continue
        commands.append(line)

    else:
        return

    return commands





def create_project_dir(language: str):
    os.chdir(Path(PROJECTS_DIR / language))



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project_title")
    parser.add_argument("language")
    parser.add_argument("config")
    info = parser.parse_args()
    args = Args(info.project_title, info.language, info.config)
    print(get_pre_make_commands(args))


    



if __name__ == "__main__":
    main()
