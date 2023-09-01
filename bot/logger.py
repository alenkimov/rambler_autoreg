import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Literal
from tqdm.asyncio import tqdm

from loguru import logger


LoggingLevel = Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "SUCCESS"]

FILE_LOG_FORMAT = "<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <white>{message}</white>"
CONSOLE_LOG_FORMAT = "<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <white>{message}</white>"


class InterceptHandler(logging.Handler):
    LEVELS_MAP = {
        logging.CRITICAL: "CRITICAL",
        logging.ERROR: "ERROR",
        logging.WARNING: "WARNING",
        logging.INFO: "INFO",
        logging.DEBUG: "DEBUG",
    }

    def _get_level(self, record):
        return self.LEVELS_MAP.get(record.levelno, record.levelno)

    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(self._get_level(record), record.getMessage())


def setup_logger(log_dir: Path, level: LoggingLevel = "DEBUG"):
    log_dir.mkdir(exist_ok=True)
    logger.remove()
    log_filename = f"{datetime.now().strftime('%d-%m-%Y')}.log"
    log_filepath = Path(log_dir, log_filename)
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
    logger.add(log_filepath, format=FILE_LOG_FORMAT, level=level, rotation='1 day')
    logger.add(lambda msg: tqdm.write(msg, end=''), colorize=True, format=CONSOLE_LOG_FORMAT, level=level)
