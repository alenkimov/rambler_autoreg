from datetime import date, datetime
import re

# Third-party libraries
from pydantic import BaseModel, validator, root_validator

# Libraries of this project
from rambler_autoreg.rambler.api import email_is_available


DOMAINS = ('@autorambler.ru', '@lenta.ru', '@myrambler.ru', '@rambler.ru', '@rambler.ua', '@ro.ru')
GENDERS = ('Male', 'Female')


class RamblerAccount(BaseModel):
    is_registered: bool = False
    imap_is_activated: bool = False
    registration_datetime: datetime = None
    login:     str
    domain:    str
    password:  str  = None
    secret:    str  = None
    gender:    str  = None
    firstname: str  = None
    lastname:  str  = None
    birthday:  date = None

    def email(self):
        if self.domain is not None:
            return f'{self.login}{self.domain}'

    @validator('login')
    def check_login(cls, login):
        if not (8 <= len(login) <= 32):
            raise ValueError('Login must contain from 8 to 32 characters')
        return login

    @validator('domain')
    def check_domain(cls, domain):
        if domain not in DOMAINS:
            raise ValueError(f"Domain can only be one of these: {DOMAINS}")
        return domain

    @root_validator
    def check_email(cls, values):
        login = values.get('login')
        domain = values.get('domain')
        if not email_is_available(f'{login}{domain}'):
            raise ValueError('Email is unavailable')
        return values

    @validator('password')
    def check_password(cls, password):
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

    @validator('secret')
    def check_secret(cls, secret):
        if not (6 <= len(secret) <= 32):
            raise ValueError('Security code must contain from 6 to 32 characters')
        return secret

    @validator('gender')
    def check_gender(cls, gender):
        if gender not in GENDERS:
            raise ValueError(f"Gender can only be one of these: {GENDERS}")
        return gender
