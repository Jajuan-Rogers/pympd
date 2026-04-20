import json
from pathlib import Path
from os import chdir
from shlex import join
import subprocess
from typing import cast
import sys
from rich.style import Style
from custom_types import  Languages, Config
import shutil 
from rich.prompt import Confirm
from rich.text import Text
from rich.console import Console
import argparse

console = Console(color_system="truecolor")

DEFAULT_CONFIG = Path(__file__).resolve().parent / "mpd.json"
CONFIG_DIR = Path.home() / ".config" / "mpd" 
CONFIG_FP = Path.home() / ".config" / "mpd" / "mpd.json"
MPD_LOG_FP = Path.home() / ".config" / "mpd" / "mpd_log.log"
EXAMPLE_FILES_DIR = Path.home() / ".config" / "mpd" / "example_files"


def no_example_dir_prompt():
    rel_exmaple_dir = EXAMPLE_FILES_DIR.relative_to(Path.home()).as_posix()
    console.print(f"ERROR: you have not set up the {rel_exmaple_dir}!")
    return Confirm.ask("would you like to create it with the default structs ?")



def get_example_config(language: Languages, config: str, project_dir: Path ):
    if not EXAMPLE_FILES_DIR.exists():
        if not no_example_dir_prompt():
            sys.exit()
    attempted_path = (EXAMPLE_FILES_DIR / language / config)
    if attempted_path.exists():
        console.print(f"[bold #1DE000]copying {config} config")
        try:
            project_dir.mkdir()
        except FileExistsError:
            console.print(f"{attempted_path.as_posix()} already exist")
            can_overwrite = Confirm.ask("\nwould you like to overwrite it ?")
            chdir(project_dir.absolute())
            shutil.copytree(attempted_path, project_dir, dirs_exist_ok=can_overwrite)
    else:
        attempted_path = attempted_path.relative_to(Path.home()).as_posix()
        console.print(f"[bold #DB6A00]{attempted_path}[/] [#DB001F]does not exist !")
        sys.exit()







def check_for_config():
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir()
        EXAMPLE_FILES_DIR.mkdir()
        MPD_LOG_FP.touch()
        return False
    return True


def setup():
    args = setup_parser()
    if not check_for_config():
        rel_config_dir = Path.joinpath(Path.home(), CONFIG_DIR.relative_to(Path.home())).as_posix()
        rel_examples_dir = Path.joinpath(Path.home(), EXAMPLE_FILES_DIR.relative_to(Path.home())).as_posix()
        console.print(f"setting up {rel_config_dir}")
        console.print(f"since {rel_config_dir} was just created you will need to",
                      f"\nsetup the {rel_examples_dir} using the structure as shown in [#8BDB00]pympd --help")

    return args
        

def setup_parser():
    parser = argparse.ArgumentParser("MPD")
    parser.add_argument("project_title")
    parser.add_argument("language")
    parser.add_argument("language_config", nargs="?", default="default")
    return parser.parse_args()



def main():
    args = setup()
    language = args.language
    config = args.language_config
    project_dir: Path = Path.cwd() / args.project_title
    get_example_config(language, config, project_dir)
        

if __name__ == "__main__":
    main()
