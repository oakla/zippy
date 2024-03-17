import toml
import logging
from zippy import path_management

logger = logging.getLogger(__name__)

config_file_path = path_management.config_file_path


class Settings:

    @classmethod
    def best_practice(cls) -> bool:
        return cls.load_setting_dict()['behaviour']['best_practice']


    @classmethod
    def winzip_cli_path(cls): 
        return cls.load_setting_dict()['paths']['winzip_cli_path']
    

    @classmethod
    def load_setting_dict(cls):
        return toml.load(config_file_path)
