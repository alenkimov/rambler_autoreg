from random import choice
import re

# Third-party libraries
from playwright.sync_api import Page

# Libraries of this project
from rambler_autoreg.logger import logger
from rambler_autoreg.captcha_services import SERVICE_CLASSES, SERVICE_NAMES, CaptchaService


class NoAPIKeysError(Exception):
    pass


class Solver:
    def __init__(self, api_keys: dict = None, service_name: str = None):
        self._services: dict[str: CaptchaService] = {}
        self._service: CaptchaService or None = None
        if api_keys is not None:
            self.set_api_keys(api_keys)
            try:
                self.change_service(service_name)
            except NoAPIKeysError as e:
                logger.error(e)
                raise

    def set_api_key(self, service_name: str, api_key: str):
        if service_name not in SERVICE_NAMES:
            raise ValueError(f'Не удалось установить новый API ключ для сервиса {service_name}: '
                             f'сервиса с таким именем не существует')
        self._services.update({service_name: SERVICE_CLASSES[service_name](api_key)})

    def set_api_keys(self, api_keys: dict[str, str]):
        for service_name, api_key in api_keys.items():
            try:
                self.set_api_key(service_name, api_key)
            except ValueError as e:
                logger.error(e)

    def change_service(self, service_name: str = None):
        """
        :param service_name: Имя сервиса.
        Доступные имена сервисов содержаться в списке rambler.captcha_service.SERVICE_NAMES
        :return: Изменился сервис, или нет
        """
        if not self._services:
            raise NoAPIKeysError(f'There are no services. '
                                 f'Set at least one api key and try again')
        if service_name is None:
            service_name = choice(list(self._services))
        elif service_name not in SERVICE_NAMES:
            raise ValueError(f'Не удалось установить сервис {service_name}: '
                             f'сервиса с таким именем не существует')
        elif service_name not in self._services:
            raise NoAPIKeysError(f'Не удалось установить сервис {service_name}: '
                                 f'отсутствует API ключ')
        self._service = self._services[service_name]

    def solve(self, page: Page):
        if self._service is None:
            raise NoAPIKeysError(f'There is no service to solve the captcha. '
                                 f'Set at least one api key and try again')

        frame = page.wait_for_selector('iframe[data-hcaptcha-widget-id]')
        url = frame.get_attribute('src')
        sitekey = re.search(r'sitekey=([\w-]+)', url).group(1)
        code = self._service.solve(page.url, sitekey)
        page.evaluate(
            'args => args[0].setAttribute("data-hcaptcha-response", args[1])',
            [frame, code],
        )
        page.evaluate(
            'args => document.querySelector(args[0]).value = args[1]',
            ['textarea[name=h-captcha-response]', code],
        )
        page.evaluate('code => hcaptcha.submit(code)', code)
        page.wait_for_timeout(500)

    def balance(self):
        if not self._services:
            raise NoAPIKeysError(f'There are no services. '
                                 f'Set at least one api key and try again')
        return self._service.balance()
