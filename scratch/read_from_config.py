
import configparser
from pathlib import Path
import re
import tomlkit
import toml

def read_from_config(config_file_path:Path):
    """
    Read a config file and return a dictionary of settings.
    """
    config = configparser.ConfigParser()
    config.read(config_file_path)
    return config


def read_toml(toml_file_path:Path):
    """
    Read a toml file and return a dictionary of settings.
    """
    return toml.load(toml_file_path)

def write_toml(toml_file_path:Path, data:dict):
    """
    Read a toml file and return a dictionary of settings.
    """
    with open(toml_file_path, 'w') as fp:
        toml.dump(data, fp)

def edit_toml(toml_file_path:Path, data:dict):
    """
    Read a toml file and return a dictionary of settings.
    """
    with open(toml_file_path, 'w') as fp:
        fp.write(tomlkit.dumps(data))

def read_tomlkit(toml_file_path:Path):
    """
    Read a toml file and return a dictionary of settings.
    """
    import tomlkit
    with open(toml_file_path, 'r') as fp:
        return tomlkit.parse(fp.read())
    

# config_dict = {
#     "DEFAULT": {
#         "winzip_cli_path": r"c:\program files\winzip\wzzip",
#     }
# }

# write_toml(Path("config.toml"), config_dict)

config_dict = toml.load(Path(r"src\config.toml"))

print(config_dict)

custom_settings = config_dict.get("CUSTOM")
print(custom_settings)

# config_dict.get(["custom"]["winzip_cli_path"] = r"c:\program files\winzip_2\whatever\wzzip"

edit_toml(Path(r"src\config.toml"), config_dict)