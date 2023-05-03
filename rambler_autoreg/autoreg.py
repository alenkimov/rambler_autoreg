from playwright._impl._api_types import TimeoutError
from datetime import datetime

from rambler_autoreg.logger import logger
from rambler_autoreg.rambler.playwright.captcha_solver import Solver
from rambler_autoreg.rambler.playwright.api import PlaywrightRamblerAPI
from rambler_autoreg.rambler.account_model import RamblerAccount
from rambler_autoreg.rambler.account_creator import generate_rambler_account
from rambler_autoreg.captcha_services import CaptchaServiceError


def autoreger(solver: Solver,
              count:    int = 1,
              login:    str = None,  # random
              domain:   str = None,  # default
              password: str = None,  # random
              secret:   str = None,  # random
              *,
              activate_imap: bool = False,
              headed:        bool = False,
              ) -> RamblerAccount or None:
    """Simple generator that automatically register rambler accounts.

    :param count: Number of accounts
    :param login: Login (before @)
    :param password: Password must contain from 8 to 32 characters,
    include at least one upper-case letter, one
    lower-case letter, and one number. You can use these
    characters: ! @ $ % ^ & * ( ) _ - +
    :param secret: Security code
    :param domain: Mail domain
    :param activate_imap: Activate IMAP or not
    :param headed: Headed режим браузера
    """
    logger.info(f'Accounts to register: {count}')
    with PlaywrightRamblerAPI(solver, headed=headed) as rambler_api:
        for i in range(count):
            start = datetime.now()
            logger.info(f'Account number {i + 1}..')
            account: RamblerAccount or None = generate_rambler_account(f'{login}{i + 1}' if login is not None else None,
                                                                           domain, password, secret)
            if account is not None:
                try:
                    rambler_api.register(account, activate_imap=activate_imap)
                    finish = datetime.now()
                    delta = finish - start
                    logger.success(f'Account number {i + 1} was successfully registered in {delta.seconds} seconds')
                except TimeoutError:
                    logger.error(f'Account number {i + 1} was not registered: Timeout 30 seconds exceeded')
                except CaptchaServiceError:
                    logger.error(f'Account number {i + 1} was not registered: Captcha service error')
                except Exception as error:
                    logger.error(f'Account number {i + 1} was not registered')
                    logger.exception(error)
                yield account
            else:
                logger.error(f'Account number {i + 1} was not registered: Wrong data')
                yield None
