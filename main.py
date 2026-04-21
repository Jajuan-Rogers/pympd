from pathlib import Path
import subprocess
import sys
from typing import Literal
import shutil 
from rich.panel import Panel
from rich.prompt import Confirm
from rich.console import Console
import argparse

console = Console(color_system="truecolor")

Languages = Literal[
    "python",     
    "javaScript", 
    "typeScript", 
    "java",       
    "c#",         
    "c++",        
    "c",          
    "rust",       
    "go",         
    "swift",      
    "kotlin",     
    "php",        
    "sql",        
    "ruby",       
    "dart"        
]

DEFAULT_CONFIG = Path(__file__).resolve().parent / "mpd.json"
CONFIG_DIR = Path.home() / ".config" / "mpd" 
CONFIG_FP = Path.home() / ".config" / "mpd" / "mpd.json"
MPD_LOG_FP = Path.home() / ".config" / "mpd" / "mpd_log.log"
EXAMPLE_FILES_DIR = Path.home() / ".config" / "mpd" / "examples"

def get_commands(commands_fp: Path, command_set: Literal["PRE:", "POST:"]) -> None:
    commands = commands_fp.read_text("utf-8").splitlines()
    commands = [c.strip() for c in commands]

    try:
        if command_set != "PRE:":
            START, STOP = commands.index("POST:"), len(commands) 
        else:
            START, STOP = 0, commands.index("POST:")
    except ValueError:
        console.print(f"ERROR: the .commands.txt file for {commands_fp.parent.name} example config missing pre or post key(s)")
        console.line()
        return

    for command in commands[START:STOP]:
        if "rm" in command:
            console.print("mpd cannot run rm, skipping")
            continue
        console.print(f"[bold #1DE000]{command}")
        # subprocess.run([*command.split()])


def get_example_config(language: Languages, config: str, project_dir: Path):
    if not EXAMPLE_FILES_DIR.exists():
        rel_exmaple_dir = EXAMPLE_FILES_DIR.relative_to(Path.home()).as_posix()
        console.print(f"ERROR: you have not set up the {rel_exmaple_dir}!")
        sys.exit()

    attempted_path = EXAMPLE_FILES_DIR / language / config

    if not attempted_path.exists():
        attempted_path = attempted_path.relative_to(Path.home()).as_posix()
        console.print(f"[bold #DB6A00]{attempted_path}[/] [#DB001F]does not exist !")
        sys.exit()

    elif project_dir.exists():
        console.print(f"[bold #1DE000]copying {config} config")
        console.print(f"{project_dir.as_posix()} already exist")
        can_overwrite = Confirm.ask(
            f"\nwould you like to overwrite {project_dir.name} ?"
        )
        if can_overwrite:
            console.print(
                Panel(
                    "[bold #DB6A00]ARE YOU SURE ?[/]\n[bold #DB001F blink](THIS CANNOT BE UNDONE)"
                )
            )
            can_overwrite = Confirm.ask()

        if not can_overwrite:
            sys.exit()

        shutil.copytree(attempted_path, project_dir, dirs_exist_ok=can_overwrite)

    elif not project_dir.exists():
        commands_fp = project_dir / ".commands.txt"
        if commands_fp.exists():
            get_commands(commands_fp, "PRE:")
        shutil.copytree(attempted_path, project_dir)



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
