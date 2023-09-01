import random
import re
import string
from datetime import date, datetime
from typing import Literal

import pyuseragents
from better_automation.utils import generate_nickname
from faker import Faker

RAMBLER_DOMAINS = ("@autorambler.ru", "@myrambler.ru", "@rambler.ru", "@rambler.ua", "@ro.ru")
RamblerDomain = Literal["@autorambler.ru", "@myrambler.ru", "@rambler.ru", "@rambler.ua", "@ro.ru"]
GENDERS = ("Male", "Female")
Gender = Literal["Male", "Female"]

ALPHABET = string.ascii_letters + string.digits


class RamblerAccount:
    def __init__(
            self,
            login: str,
            password: str,
            secret: str,
            domain: RamblerDomain = "@rambler.ru",
            gender: Gender = None,
            firstname: str = None,
            lastname: str = None,
            birthday: date = None,
            useragent: str = None,
            number: int = None,
            hide_email: bool = False,
    ):
        self.login = login
        self.password = password
        self.secret = secret
        self.domain = domain
        self.gender = gender
        self.firstname = firstname
        self.lastname = lastname
        self.birthday = birthday
        self.imap_is_activated: bool = False
        self.additional_info_is_registered: bool = False
        self.registration_datetime: datetime | None = None

        self._check_password(password)

        self.useragent: str = useragent
        self.number = number

        self.hide_email = hide_email

    def __repr__(self):
        email = self.short_email if self.hide_email else self.email
        return f"RamblerAccount(email={email})"

    def __str__(self):
        email = self.short_email if self.hide_email else self.email
        if self.number:
            return f"[{self.number:04}] [{email}]"
        return f"[{email}]"

    @property
    def is_registered(self) -> bool:
        return self.registration_datetime is not None

    @property
    def email(self) -> str:
        return f'{self.login}{self.domain}'

    @property
    def short_email(self) -> str:
        return f'{self.login[0]}***{self.login[-1]}{self.domain}'

    @staticmethod
    def _check_password(password):
        """
        Password must contain from 8 to 32 characters,
        include at least one uppercase letter, one
        lowercase letter, and one number. You can use these
        characters: ! @ $ % ^ & * ( ) _ - +
        """
        if not (8 <= len(password) <= 32):
            raise ValueError('Password must contain from 8 to 32 characters')
        elif re.search('[0-9]', password) is None:
            raise ValueError('Password must contain a number')
        elif re.search('[a-z]', password) is None:
            raise ValueError('Password must contain an lower-case letter')
        elif re.search('[A-Z]', password) is None:
            raise ValueError('Password must contain an upper-case letter')
        elif re.search('\?', password) is not None:
            raise ValueError('Password cannot contain the ? character, '
                             'only these characters: ! @ $ % ^ & * ( ) _ - +')
        return password

    @staticmethod
    def _generate_login(length: int) -> str:
        while True:
            login = generate_nickname(length, numbers=True, signs=True)
            if re.match('^[a-zA-Z0-9]', login[0]) and re.match('[a-zA-Z0-9]$', login[-1]):
                return login

    @staticmethod
    def _generate_birthday():
        """Генерация случайной даты с 1970г. по 2000г."""
        start_date = date(year=1970, month=1, day=1).toordinal()
        end_date = date(year=2000, month=1, day=1).toordinal()
        birthday = date.fromordinal(random.randint(start_date, end_date))
        return birthday

    @staticmethod
    def _generate_password(length: int) -> str:
        if not (8 <= length <= 32):
            raise ValueError(f'Password length must be from 8 to 32, not {length}.')

        special_characters = "!@$%^&*()_-+"
        alphabet = string.ascii_letters + string.digits + special_characters

        password = (
                random.choice(string.ascii_lowercase)
                + random.choice(string.ascii_uppercase)
                + random.choice(string.digits)
                + random.choice(special_characters)
        )

        password += ''.join(random.choice(alphabet) for _ in range(length - 4))
        return ''.join(random.sample(password, len(password)))

    @staticmethod
    def _generate_name(locale: str, gender: Gender) -> tuple[str, str]:
        """Генерация случайных имени и фамилии в зависимости от заданных пола и локали"""
        fake = Faker(locale)
        firstname = fake.first_name_male() if gender == 'Male' else fake.first_name_female()
        lastname = fake.last_name_male() if gender == 'Male' else fake.last_name_female()
        return firstname, lastname

    @classmethod
    def generate(
            cls,
            *,
            locale: str = "en_US",
            login_length: int = 12,
            password_length: int = 12,
            secret_length: int = 8,
            gender: Gender = "Male",
            domain: RamblerDomain = "@rambler.ru",
            number: int = None,
            hide_email: bool = False,
    ):
        data = {
            'domain': domain,
            'gender': gender,
            'login': cls._generate_login(login_length),
            'password': cls._generate_password(password_length),
            'secret': cls._generate_password(secret_length),
            'birthday': cls._generate_birthday(),
            'useragent': pyuseragents.random(),
            'number': number,
            'hide_email': hide_email,
        }
        data['firstname'], data['lastname'] = cls._generate_name(locale, gender)
        return cls(**data)
