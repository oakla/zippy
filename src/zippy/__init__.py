import os
import logging
from .zip import Zippy
from . import checks

# Define the directory for the log files
home_path = os.path.expanduser("~")
log_dir = os.path.join(home_path, "autobots", "zippy", "logs")
os.makedirs(log_dir, exist_ok=True)

log_levels = ["debug", "info", "warning"]
handlers = []

for level in log_levels:
    # Create a file handler
    file_handler = logging.FileHandler(os.path.join(log_dir, f"{level}.log"))
    
    # Set the log level
    file_handler.setLevel(getattr(logging, level.upper()))
    
    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s')
    
    # Add the formatter to the file handler
    file_handler.setFormatter(formatter)

    handlers.append(file_handler)

logging.basicConfig(
    level="DEBUG",
    handlers=handlers
)