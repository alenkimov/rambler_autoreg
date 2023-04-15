"""Настройка логера Loguru"""
from loguru import logger
from datetime import datetime
import sys

# Third-party libraries
# -- There are no libraries here

# Libraries of this project
from rambler_autoreg.paths import LOG_DIR


DEBUG = True

FILE_LOG_FORMAT = "<white>{time:YYYY-MM-DD HH:mm:ss}</white> | <level>{level: <8}</level> | <white>{message}</white>"
CONSOLE_LOG_FORMAT = "<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <white>{message}</white>"


def setup(debug: bool):
    logger.remove()
    log_file_name = f'{datetime.now().strftime("%d-%m-%Y")}.log'
    log_file_path = LOG_DIR / log_file_name
    logger.add(log_file_path, format=FILE_LOG_FORMAT, level="DEBUG", rotation='1 day')
    logger.add(sys.stderr, colorize=True, format=CONSOLE_LOG_FORMAT, level='DEBUG' if debug else 'INFO')


setup(DEBUG)
