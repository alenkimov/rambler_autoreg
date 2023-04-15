from abc import ABC, abstractmethod

# Third-party libraries
# -- ruCaptcha
from twocaptcha import TwoCaptcha as RucaptchaClient
from twocaptcha.api import ApiException as RucaptchaException
# -- AntiCaptcha
from python_anticaptcha import AnticaptchaClient, HCaptchaTaskProxyless
from python_anticaptcha.exceptions import AnticaptchaException

# Libraries of this project
from rambler_autoreg.logger import logger


class CaptchaServiceError(Exception):
    def __init__(self, service_name, message):
        self.service_name = service_name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'[service: {self.service_name}] {self.message}'


class CaptchaService(ABC):
    name: str = 'AbstractCaptchaService'

    @abstractmethod
    def __init__(self, api_key: str):
        pass

    @abstractmethod
    def _solve(self, url: str, sitekey: str):
        pass

    @abstractmethod
    def _balance(self) -> float:
        pass

    def solve(self, url: str, sitekey: str):
        logger.info(f'Solving captcha with {self.name}. url: {url}')
        try:
            return self._solve(url, sitekey)
        except Exception as e:
            raise CaptchaServiceError(self.name, e)

    def balance(self) -> float:
        try:
            return self._balance()
        except Exception as e:
            raise CaptchaServiceError(self.name, e)


class RucaptchaService(CaptchaService):
    name = 'ruCaptcha'

    def __init__(self, api_key: str):
        self.client = RucaptchaClient(api_key)

    def _solve(self, url: str, sitekey: str) -> str:
        code = self.client.hcaptcha(sitekey, url)['code']
        return code

    def _balance(self) -> float:
        return self.client.balance()


class AnticaptchaService(CaptchaService):
    name = 'AntiCaptcha'

    def __init__(self, api_key: str):
        self.client = AnticaptchaClient(api_key)

    def _solve(self, url: str, sitekey: str) -> str:
        task = HCaptchaTaskProxyless(url, sitekey)
        job = self.client.createTask(task)
        job.join()
        code = job.get_solution_response()
        return code

    def _balance(self) -> float:
        return self.client.getBalance()


# SERVICE_CLASSES = {'ruCaptcha': RucaptchaService, 'AntiCaptcha': AnticaptchaService}
SERVICE_CLASSES = {service.name: service for service in (RucaptchaService, AnticaptchaService)}
SERVICE_NAMES = list(SERVICE_CLASSES.keys())
