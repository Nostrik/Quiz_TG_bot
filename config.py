import logging
import colorlog

LOG_LEVEL = logging.INFO
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    "%(yellow)s%(asctime)s - %(log_color)s%(levelname)s%(reset)s - %(purple)s%(message)s",
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'white',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    }
))

logger = logging.getLogger()

if not logger.handlers:
    logger.addHandler(handler)

logger.setLevel(LOG_LEVEL)

def setup_logging():
    pass
