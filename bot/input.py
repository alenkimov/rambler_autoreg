from better_proxy import Proxy

from bot.paths import INPUT_DIR

PROXIES_TXT = INPUT_DIR / "proxies.txt"
PROXIES_TXT.touch(exist_ok=True)
PROXIES = Proxy.from_file(PROXIES_TXT)
