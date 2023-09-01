from collections import defaultdict
from math import ceil
from typing import Iterable
import asyncio
import random

import aiohttp
from better_automation.anticaptcha import AnticaptchaClient
from better_automation.utils.other import bounded_gather
from better_proxy import Proxy

from bot.config import CONFIG
from bot.input import PROXIES
from bot.logger import logger
from bot.output import write_txt, write_csv
from bot.rambler import PlaywrightRamblerAPI, RamblerAccount


async def register_account(
        rambler: PlaywrightRamblerAPI,
        anticaptcha: AnticaptchaClient,
        account: RamblerAccount,
        *,
        proxy: Proxy = None,
        activate_imap: bool = False,
):
    await rambler.register(account, anticaptcha, proxy=proxy, activate_imap=activate_imap)
    if account.is_registered:
        write_txt(account, filename="accounts_imap" if account.imap_is_activated else "accounts")
        write_csv(account, filename="accounts_imap" if account.imap_is_activated else "accounts",
                  proxy=proxy.as_url if proxy else None)


async def _register_accounts(
        rambler: PlaywrightRamblerAPI,
        anticaptcha: AnticaptchaClient,
        accounts: Iterable[RamblerAccount],
        proxy: Proxy = None,
        activate_imap: bool = False,
        ignore_errors: bool = True,
):
    for account in accounts:
        if ignore_errors:
            try:
                await register_account(rambler, anticaptcha, account,
                                       proxy=proxy, activate_imap=activate_imap)
            except Exception as e:
                logger.error(f"{account} Account was skipped: {e}")
                continue
        else:
            await register_account(rambler, anticaptcha, account,
                                   proxy=proxy, activate_imap=activate_imap)
        sleep_time = random.randrange(*CONFIG.DELAY_RANGE) if sum(CONFIG.DELAY_RANGE) > 0 else 0
        if sleep_time > 0:
            logger.info(f"{account} Sleep ({sleep_time}) secs")
            await asyncio.sleep(sleep_time)


async def register_accounts(count: int = 1, activate_imap: bool = False):
    proxies = tuple()
    if PROXIES:
        proxies = tuple(set(PROXIES))
        proxy_count = len(proxies)
        logger.info(f"Loaded {proxy_count} unique proxies")

    logger.info(f"Generating accounts...")
    accounts = [RamblerAccount.generate(number=i + 1, hide_email=CONFIG.HIDE_SECRETS) for i in range(count)]
    logger.info(f"Generated {len(accounts)} accounts")

    proxy_to_accounts: defaultdict[str | None: list[RamblerAccount]] = defaultdict(list)

    async with aiohttp.ClientSession() as session, PlaywrightRamblerAPI(
            headless=CONFIG.HEADLESS, proxy=proxies[0] if proxies else None) as rambler:
        anticaptcha = AnticaptchaClient(session, CONFIG.ANTICAPTCHA_API_KEY)
        balance = await anticaptcha.request_balance()
        logger.info(f"Anticaptcha balance: ${balance}")
        if proxies:
            for i, account in enumerate(accounts):
                proxy = proxies[i % len(proxies)]
                proxy_to_accounts[proxy].append(account)
            tasks = [_register_accounts(rambler, anticaptcha, accounts, proxy, activate_imap, CONFIG.IGNORE_ERRORS)
                     for proxy, accounts in proxy_to_accounts.items()]
        else:
            chunk_size = ceil(len(accounts) / CONFIG.MAX_TASKS)
            account_chunks = [accounts[i:i + chunk_size] for i in range(0, len(accounts), chunk_size)]
            tasks = [_register_accounts(rambler, anticaptcha, chunk, None, activate_imap, CONFIG.IGNORE_ERRORS)
                     for chunk in account_chunks]

        await bounded_gather(tasks, CONFIG.MAX_TASKS)
