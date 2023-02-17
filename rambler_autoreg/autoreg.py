# Third-party libraries
# -- There are no libraries here

# Libraries of this project
from logger import logger
from rambler.playwright.captcha_solver import Solver
from rambler.playwright.api import PlaywrightRamblerAPI
from rambler.account_model import RamblerAccount
from rambler.account_creator import generate_rambler_account


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
            logger.info(f'Account number {i + 1}..')
            account: RamblerAccount or None = generate_rambler_account(f'{login}{i + 1}' if login is not None else None,
                                                                       domain, password, secret)
            rambler_api.register(account, activate_imap=activate_imap)
            logger.success(f'Account number {i + 1} was successfully registered')
            yield account
