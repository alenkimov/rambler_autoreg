from datetime import date, datetime

# Third-party libraries
from playwright.sync_api import sync_playwright, BrowserContext, Page
from playwright._impl._api_types import TimeoutError as PlaywrightTimeoutError

# Libraries of this project
from logger import logger
from definitions import JS_DIR
from rambler.playwright.captcha_solver import Solver
from rambler.account_model import RamblerAccount

HCAPTCHA_SCRIPT_FILE_PATH = JS_DIR / 'hcaptcha.js'

GENDER_TO_PLACEHOLDER = {'Male': 'Мужской', 'Female': 'Женский'}
MONTH_NUMBER_TO_PLACEHOLDER = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь"
}


class PlaywrightRamblerAPI:
    def __init__(self, solver: Solver, headed: bool = False):
        self._playwright = sync_playwright().start()
        self._solver = solver
        self._browser = self._playwright.chromium.launch(headless=not headed)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._playwright.stop()

    def _activate_imap(self, context: BrowserContext):
        logger.info('IMAP activation..')

        # Новая вкладка
        page = context.new_page()
        page.goto('https://mail.rambler.ru/settings/mailapps')

        # Закрываем попап-сообщение
        page.wait_for_selector('.rui-Popup-close').click()

        # Активируем IMAP
        page.get_by_role('button', name='Вкл').click()
        page.goto('https://mail.rambler.ru/settings/mailapps/change')

        # Решаем капчу
        self._solver.solve(page)

        # Подтверждаем активацию IMAP
        page.get_by_role('button', name='Отправить').click()

        # Зачем-то ждем полсекунды
        page.wait_for_timeout(500)

    def _register(self, context: BrowserContext,
                  login: str, domain: str, password: str, secret: str,
                  gender: str, firstname: str, lastname: str, birthday: date, activate_imap: bool):
        logger.info(
            f'Registering account. mail: {login}{domain} | pass: {password} | secret: {secret} | activate_imap: {activate_imap}')

        # Новая вкладка
        page = context.new_page()
        page.goto('https://id.rambler.ru/login-20/mail-registration')

        # Ввод логина и выбор домена
        page.locator('#login').type(login)
        page.locator('input[value="@rambler.ru"]').click()
        page.get_by_text(domain).click()

        # Ввод пароля
        page.locator('#newPassword').type(password)
        page.locator('#confirmPassword').type(password)

        # Выбор и ввод секретного вопроса
        page.get_by_placeholder("Выберите вопрос").click()
        page.get_by_text("Кличка домашнего животного").click()
        page.locator('#answer').type(secret)

        # Решение капчи
        self._solver.solve(page)
        try:
            page.click("button[type=submit]")
        except PlaywrightTimeoutError:
            logger.error(f'')

        # Ввод имени и фамилии
        page.locator("#firstname").type(firstname)
        page.locator("#lastname").type(lastname)

        # Выбор пола
        page.locator('#gender').click()
        page.get_by_text(GENDER_TO_PLACEHOLDER[gender]).click()

        # Ввод дня рождения
        page.get_by_placeholder('День').click()
        page.get_by_text(str(birthday.day), exact=True).click()

        # Ввод месяца рождения
        page.get_by_placeholder("Месяц").click()
        page.get_by_text(MONTH_NUMBER_TO_PLACEHOLDER[birthday.month], exact=True).click()

        # Ввод года рождения
        page.get_by_placeholder("Год").click()
        page.get_by_text(str(birthday.year), exact=True).click()

        # Отправка формы
        page.click("button[type=submit]")
        page.wait_for_timeout(500)

        # Активация IMAP
        if activate_imap: self._activate_imap(context)

    def register(self, account: RamblerAccount, *, activate_imap: bool = False):
        if account.is_registered:
            logger.warning(f'Account {account} is already registered')
            return
        context = self._browser.new_context()
        context.add_init_script(path=HCAPTCHA_SCRIPT_FILE_PATH)  # Скрипт для решения hCaptcha
        self._register(context,
                       account.login, account.domain, account.password, account.secret,
                       account.gender, account.firstname, account.lastname, account.birthday,
                       activate_imap=activate_imap)
        context.close()
        account.is_registered = True
        account.registration_datetime = datetime.now()
        if activate_imap: account.imap_is_activated = True
