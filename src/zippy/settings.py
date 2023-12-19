import toml
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


WORDS_FILE_NAME = r"eff.org_files_2016_07_18_eff_large_wordlist.txt"
words_file_path = Path(__file__).resolve().with_name(WORDS_FILE_NAME)
CONFIG_FILE = r"config.toml"
config_file_path = Path(__file__).resolve().with_name(CONFIG_FILE)


class ConfigKeys:
    WINZIP_CLI_PATH = "winzip_cli_path"
    PROMPT_USER_SELECTION_OF_WINZIP_CLI_PATH = "prompt_user_selection_of_winzip_cli_path"


class Settings:

    @classmethod
    @property
    def phrase_words_file_path(cls):
        return words_file_path


    @classmethod
    @property
    def winzip_cli_path(cls): 
        return cls.setting_dict()['winzip_cli_path']
    

    @classmethod
    def setting_dict(cls):
        default_settings = cls.get_default_settings()
        if default_settings is None:
            message = f"No default settings table found in config file ({CONFIG_FILE})."
            logger.error(message)
            raise Exception(message)
        settings = default_settings.copy()
        
        custom_settings = cls.get_custom_settings()
        if custom_settings is None:
            return settings

        for custom_setting_key, custom_setting_value in custom_settings.items():
            settings[custom_setting_key] = custom_setting_value

        return settings

    @classmethod
    @property
    def prompt_user_selection_of_winzip_cli_path(cls) -> bool:
        logger.debug("Checking config to see if user should be asked to select WinZip path.")
        return_bool = cls.setting_dict()[ConfigKeys.PROMPT_USER_SELECTION_OF_WINZIP_CLI_PATH]
        logger.debug(f"{ConfigKeys.PROMPT_USER_SELECTION_OF_WINZIP_CLI_PATH} is set to {return_bool}")
        return return_bool


    @classmethod
    @property
    def config_file_path(cls):
        return config_file_path


    @classmethod
    def load_config_dict(cls):
        return toml.load(config_file_path)
    

    @classmethod
    def get_custom_settings(cls):
        return cls.load_config_dict().get("CUSTOM")


    @classmethod
    def get_default_settings(cls):
        return cls.load_config_dict().get("DEFAULT")


    @classmethod
    def overwrite_toml(cls, toml_file_path:Path, data:dict):
        with open(toml_file_path, 'w') as fp:
            toml.dump(data, fp)


    @classmethod
    def add_custom_setting(cls, key:str, value:str):
        config_dict = cls.load_config_dict()
        custom_settings = cls.get_custom_settings()
        if custom_settings is None:
            custom_settings = {}
        custom_settings[key] = value
        config_dict["CUSTOM"] = custom_settings
        cls.overwrite_toml(config_file_path, config_dict)


    @classmethod
    def save_custom_winzip_path(cls, winzip_cli_path):
        cls.add_custom_setting(ConfigKeys.WINZIP_CLI_PATH, winzip_cli_path)

