import logging
import sys

logger = logging.getLogger(__name__)


# I think this is left over from when this project used PyInstaller
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    logger.debug(
        f"`getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')` evalutated as `True`"
    )
    logger.debug("running in a PyInstaller bundle")
    print(f"sys._MEIPASS: {sys._MEIPASS}")  # type: ignore
else:
    logger.debug(
        f"`getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')` evalutated as `False`"
    )
    # print('running in a normal Python process')
    ...