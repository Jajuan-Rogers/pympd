from os import PathLike
from typing import Literal, NamedTuple, TypedDict 


class File(NamedTuple):
    """
    name: str file name with extension
    content: PathLike Path to the file that contains the contents you want,
    its recommended that these 'exmaple' files are stored in the pymd config 
    folder in the ~/.config/pympd/exmaple_files directory but they can be stored
    anywhere on your drive
    """
    name: str
    content: PathLike 

class Dir(NamedTuple):
    name: str
    files: tuple[File,...]
    dirs: tuple[PathLike[str],...]

class DirLayout(TypedDict):
    dirs: list[str]|None
    files: list[str]|None

class Config(NamedTuple):
    """
    pre_commands: tuple[str,...]|None
    place all the commands you'd like to run right after the project folder is created.
    the 'rm' command is not allowed in the tuple.

    post_commands: tuple[str,...]|None
    place all commands you'd like to run right after the entire project directory is created.
    the 'rm' command is not allowed in the tuple.

    "src": DirLayout
    DirLayout is just a dict with a 'dirs' key with Dir object value and a 'files' key with 
    File object values. This is optional, a null key for src will not create a src dir. 

    "root": DirLayout
    DirLayout is just a dict with a 'dirs' key with Dir object value and a 'files' key with 
    this is the same as src but it is not optional (if you src is None). You must provide a
    DirLayout object if you set src = None/null in config as not providing either defeats 
    the purpose of pympd
    """
    pre_commands: tuple[str,...]|None
    post_commands: tuple[str,...]|None
    src: DirLayout|None
    root: DirLayout|None

    #Note: make sure src and root are not None right after object creation


languages: set["Languages"] = {
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
}

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
