import json
from pathlib import Path
from os import chdir
import sys
from typing import cast
from custom_types import Dir, Languages, languages, Config
import shutil
from rich.console import Console
import argparse

console = Console(color_system="truecolor")

DEFAULT_CONFIG = Path(__file__).resolve().parent / "mpd.json"
CONFIG_DIR = Path.home() / ".config" / "mpd" 
CONFIG_FP = Path.home() / ".config" / "mpd" / "mpd.json"
MPD_LOG_FP = Path.home() / ".config" / "mpd" / "mpd_log.log"
EXAMPLE_FILES_DIR = Path.home() / ".config" / "mpd" / "example_files"



def build_dirs(root_dirs: list[str]):
    for dirs in root_dirs:
        outer_dir = Path.cwd() / dirs
        outer_dir.mkdir()
        console.print(f"created {outer_dir.name}")


def make_files(files: list[str], config: str):
    for file, contents_example in files: 
        if "{EXAMPLE}/{CONFIG}" not in file:
            f = Path.cwd() / file
            f.touch(exist_ok=False)
        else:
            file = Path(file)
            example_file = EXAMPLE_FILES_DIR / config / file.name
            shutil.copy(example_file, Path.cwd() / file.absolute())



            





def check_defined_dir_structs(config: Config, config_name):
    if config.root and config.root["dirs"]:
        build_dirs(config.root["dirs"])
        if (files:=config.root["files"]):
            make_files(files, config_name)
    if config.src and config.src["dirs"]:
        src_dir = Path.cwd() / "src"
        src_dir.mkdir()
        chdir(src_dir.absolute())
        build_dirs(config.src["dirs"])
        if (files:=config.src["files"]):
            make_files(files, config_name)






    ...

def copy_config_files():
    shutil.copy(DEFAULT_CONFIG, CONFIG_DIR)
    MPD_LOG_FP.touch(exist_ok=False)



def check_for_config():
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir()
        return False
    return True

def get_config(language: Languages, language_config: str):
    with CONFIG_FP.open("r") as config:
        config = json.load(config)[language][language_config] #Config(**json.load(config)[language])
        console.print(config)
    return Config(**config)


def setup():
    args = setup_parser()
    if not check_for_config():
        console.print("[bold red]COPYING CONFIG CONTENTS")
        copy_config_files()

    return args
        

def setup_parser():
    parser = argparse.ArgumentParser("MPD")
    parser.add_argument("project_title")
    parser.add_argument("language")
    parser.add_argument("language_config", nargs="?", default="default")
    return parser.parse_args()



def main():
    args = setup()
    try:
        config = get_config(args.language, args.language_config)
    except TypeError as e:
        console.print("CONFIG ERROR: there was an error while reading your config", 
                      "pleae ensure the config structure is correct",
                      "see mpd --help")
        console.log(e)
    except KeyError as e:
        console.print(f"Invalid config name:  '{args.language_config}' does NOT exist in mpd.json")
        console.log(e)
    else:
        args.project_title = cast(str, args.project_title)
        project_dir = Path.cwd() / args.project_title
        project_dir.mkdir(exist_ok=False)
        chdir(project_dir.absolute())
        config_name = args.language_config
        check_defined_dir_structs(config, config_name)
        

if __name__ == "__main__":
    main()
