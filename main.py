import asyncio

import questionary

from bot.ask import ask_int
from bot.author import TG_LINK
from bot.paths import LOG_DIR
from bot.config import CONFIG, CONFIG_TOML
from bot.logger import setup_logger
from bot.scripts import register_accounts


async def main():
    setup_logger(LOG_DIR, CONFIG.LOGGING_LEVEL)
    print(f"Telegram: {TG_LINK}")
    if not CONFIG.ANTICAPTCHA_API_KEY:
        print(f"Set Anticaptcha key into config file: {CONFIG_TOML}")
        return

    count = await ask_int("How many accounts do you need to register? (int)", min=1, max=10_000)
    activate_imap = await questionary.confirm("Activate IMAP?", default=True).ask_async()
    await register_accounts(count, activate_imap)


if __name__ == '__main__':
    asyncio.run(main())
