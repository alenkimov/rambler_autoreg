from better_automation.utils import copy_file, load_toml
from pydantic import BaseModel

from bot.logger import LoggingLevel
from bot.paths import CONFIG_DIR, DEFAULT_CONFIG_DIR
from bot.rambler.account import Gender, RamblerDomain

DEFAULT_CONFIG_TOML = DEFAULT_CONFIG_DIR / "config.toml"
CONFIG_TOML = CONFIG_DIR / "config.toml"
copy_file(DEFAULT_CONFIG_TOML, CONFIG_TOML)


class Config(BaseModel):
    # Debug
    LOGGING_LEVEL: LoggingLevel = "INFO"
    IGNORE_ERRORS: bool = True
    HIDE_SECRETS: bool = True
    HEADLESS: bool = True
    # Limits
    MAX_TASKS: int = 5
    DELAY_RANGE: tuple[int, int] = (90, 150)
    # Anticaptcha
    ANTICAPTCHA_API_KEY: str
    # Defaults
    DOMAIN: RamblerDomain = "@rambler.ru"
    GENDER: Gender = "Male"
    LOCALE: str = "en_US"
    LOGIN_LENGTH: int = 16
    PASSWORD_LENGTH: int = 16
    SECRET_LENGTH: int = 12


CONFIG = Config(**load_toml(CONFIG_TOML))
