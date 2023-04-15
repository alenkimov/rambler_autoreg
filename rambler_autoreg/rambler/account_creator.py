from datetime import date
import string
import secrets
import random

# Third-party libraries
from pydantic import ValidationError
from faker import Faker
from faker.config import AVAILABLE_LOCALES

# Libraries of this project
from rambler_autoreg.logger import logger
from rambler_autoreg.rambler.account_model import RamblerAccount, GENDERS


ALPHABET = string.ascii_letters + string.digits

DEFAULT_DOMAIN = '@rambler.ru'
DEFAULT_GENDER = 'Male'
DEFAULT_LOCALE = 'ru_RU'
DEFAULT_LOGIN_LENGTH    = 12
DEFAULT_PASSWORD_LENGTH = 16
DEFAULT_SECRET_LENGTH   = 6


def generate_birthday():
    """Генерация случайной даты с 1970г. по 2000г."""
    start_date = date(year=1970, month=1, day=1).toordinal()
    end_date = date(year=2000, month=1, day=1).toordinal()
    birthday = date.fromordinal(random.randint(start_date, end_date))
    logger.debug(f'Успешно сгенерирована дата рождения: {birthday}')
    return birthday


def generate_login(length: int = DEFAULT_LOGIN_LENGTH) -> str:
    login = secrets.token_hex(length // 2)
    logger.debug(f'Успешно сгенерирован логин длины {length}: {login}')
    return login


def generate_password(length: int = DEFAULT_PASSWORD_LENGTH) -> str:
    """
    Generate a {6 <= length <= 128}-character alphanumeric password with at least one lowercase character,
    at least one uppercase character, and at least one digit

    https://docs.python.org/3/library/secrets.html#recipes-and-best-practices
    """
    if not (6 <= length <= 128):
        raise ValueError(f'Password length must be from 6 to 128, not {length}.')
    while True:
        password = ''.join(secrets.choice(ALPHABET) for _ in range(length))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)):
            logger.debug(f'Успешно сгенерирован пароль длины {length}: {password}')
            return password
        logger.debug(f'Не удалось сгенерировать пароль длины {length}, пробую снова..')


def generate_secret(length: int = DEFAULT_SECRET_LENGTH) -> str:
    secret = secrets.token_hex(length // 2)
    logger.debug(f'Успешно сгенерирован секретный код длины {length}: {secret}')
    return secret


def generate_name(locale: str = DEFAULT_LOCALE, gender: str = DEFAULT_GENDER) -> tuple[str, str]:
    """Генерация случайных имени и фамилии в зависимости от заданных пола и локали"""
    if locale not in AVAILABLE_LOCALES: locale = DEFAULT_LOCALE
    if gender not in GENDERS: gender = DEFAULT_GENDER
    fake = Faker(locale)
    firstname = fake.first_name_male() if gender == 'Male' else fake.first_name_female()
    lastname  = fake.last_name_male()  if gender == 'Male' else fake.last_name_female()
    logger.debug(f'Успешно сгенерированы имя и фамилия: {firstname} {lastname}')
    return firstname, lastname


def generate_rambler_account(login: str = None,
                             domain: str = None,
                             password: str = None,
                             secret: str = None) -> RamblerAccount or None:
    firstname, lastname = generate_name()
    data = {
        'login': login or generate_login(),
        'domain': domain or DEFAULT_DOMAIN,
        'password': password or generate_password(),
        'secret': secret or generate_secret(),
        'gender': DEFAULT_GENDER,
        'firstname': firstname,
        'lastname': lastname,
        'birthday': generate_birthday(),
    }
    try:
        return RamblerAccount(**data)
    except ValidationError as e:
        logger.exception(e)
        return None
