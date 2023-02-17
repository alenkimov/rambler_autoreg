# Third-party libraries
from pydantic import BaseSettings
import toml

# Libraries of this project
from definitions import SETTINGS_DIR


SETTINGS_TOML = SETTINGS_DIR / 'settings.toml'
API_KEYS_TOML = SETTINGS_DIR / 'api_keys.toml'


class Settings(BaseSettings):
    # -- Main --
    count: int     = 1
    service: str   = None
    # -- Registration --
    login: str     = None
    password: str  = None
    secret: str    = None
    domain: str    = '@rambler.ru'
    imap: bool     = True
    # -- Output --
    add_date: bool = True
    # -- Debug --
    debug: bool    = False
    headed: bool   = False


# Default settings
settings = Settings()


# Creating files with default settings, if there are no
with open(API_KEYS_TOML, 'a'): pass
if not SETTINGS_TOML.exists():
    with open(SETTINGS_TOML, 'w', encoding='utf-8') as settings_toml:
        toml.dump(settings.dict(), settings_toml)


# Load settings, if present
with open(SETTINGS_TOML, encoding='utf-8') as settings_toml:
    settings = Settings(**toml.load(settings_toml))

with open(API_KEYS_TOML, encoding='utf-8') as api_keys_toml:
    api_keys = toml.load(api_keys_toml)


# Saving settings funcs
def save_settings():
    with open(SETTINGS_TOML, 'w', encoding='utf-8') as settings_toml:
        toml.dump(settings.dict(), settings_toml)


def save_api_keys():
    with open(API_KEYS_TOML, 'w', encoding='utf-8') as api_keys_toml:
        toml.dump(api_keys, api_keys_toml)
