from pathlib import Path
from os import makedirs

BASE_DIR      = Path(__file__).resolve().parent.parent
SCRIPTS_DIR   = Path(__file__).resolve().parent
JS_DIR        = SCRIPTS_DIR / 'js'
SETTINGS_DIR  = BASE_DIR / 'settings'
OUTPUT_DIR    = BASE_DIR / 'output'
LOG_DIR       = BASE_DIR / 'log'

makedirs(SETTINGS_DIR, exist_ok=True)
makedirs(OUTPUT_DIR,   exist_ok=True)
makedirs(LOG_DIR,      exist_ok=True)
