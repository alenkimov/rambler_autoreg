from rambler_autoreg.config import settings, api_keys
from rambler_autoreg.rambler.playwright.captcha_solver import Solver, NoAPIKeysError
from rambler_autoreg.captcha_services import CaptchaServiceError
from rambler_autoreg.logger import setup as setup_logger
from rambler_autoreg.logger import logger
from rambler_autoreg.autoreg import autoreger
from rambler_autoreg.output import write


def main():
    try:
        solver = Solver(api_keys, settings.service)
    except NoAPIKeysError:
        return

    # Костыльный способ проверить валидность предоставленных API ключей
    try:
        balance = solver.balance()
        logger.info(f'Balance: {balance}')
    except CaptchaServiceError as e:
        logger.error(e)
        return

    setup_logger(settings.debug)
    accounts_data_to_write = []
    rambler_autoreger = autoreger(solver,
                                  count=settings.count, login=settings.login, domain=settings.domain,
                                  password=settings.password, secret=settings.secret,
                                  activate_imap=settings.imap,
                                  headed=settings.headed)
    for account in rambler_autoreger:
        data = account.dict(include={'registration_datetime', 'imap_is_activated', 'password', 'secret'})
        data.update({'email': account.email()})
        accounts_data_to_write.append(data)
    write(accounts_data_to_write, add_date=settings.add_date)
