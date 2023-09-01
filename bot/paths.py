from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent

CONFIG_DIR         = BASE_DIR / "config"
DEFAULT_CONFIG_DIR = CONFIG_DIR / ".default"
INPUT_DIR          = BASE_DIR / "input"
OUTPUT_DIR         = BASE_DIR / "output"
LOG_DIR            = BASE_DIR / "log"
JS_DIR             = SCRIPT_DIR / 'js'

for dirpath in [INPUT_DIR, OUTPUT_DIR, LOG_DIR]:
    dirpath.mkdir(exist_ok=True)
