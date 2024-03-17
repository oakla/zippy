import toml
from pathlib import Path

CONFIG_FILE = r"C:\Users\Alexander.Oakley\my-stuff-noonedrive\Code\proj\py-boom-zip\src\config.toml"
config_file_path = CONFIG_FILE

class Settings:


    @classmethod
    @property
    def config_dict(cls):
        return toml.load(config_file_path)
    a = config_dict

    @classmethod
    def some_func(cls):
        print(type(cls.config_dict))
        print(cls.config_dict)

print(Settings.a)

print(Settings.a['DEFAULT'])

Settings.some_func()