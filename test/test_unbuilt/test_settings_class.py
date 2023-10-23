import toml
from pathlib import Path
from zippy.settings import Settings

CONFIG_FILE = r"C:\Users\Alexander.Oakley\my-stuff-noonedrive\Code\proj\py-boom-zip\src\config.toml"
config_file_path = CONFIG_FILE



a = Settings.prompt_user_selection_of_winzip_cli_path
print(a)


b = Settings.winzip_cli_path
print(b)