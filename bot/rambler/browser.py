from datetime import date, datetime

from better_automation.anticaptcha import AnticaptchaClient
from better_proxy import Proxy
from playwright._impl._api_types import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import BrowserContext, Page
from playwright.async_api import async_playwright, Browser, ProxySettings
from playwright.async_api._generated import Playwright as AsyncPlaywright

from bot.logger import logger
from bot.paths import JS_DIR
from bot.rambler.account import RamblerAccount, RamblerDomain, Gender

HCAPTCHA_SCRIPT_FILE_PATH = JS_DIR / 'hcaptcha.js'

GENDER_TO_PLACEHOLDER: {Gender: str} = {'Male': 'Мужской', 'Female': 'Женский'}
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
    12: "Декабрь",
}


class PlaywrightRamblerAPI:
    REGISTRATION_HCAPTCHA_SITE_KEY = "322e5e22-3542-4638-b621-fa06db098460"
    IMAP_HCAPTCHA_SITE_KEY = "3e7d7215-1d63-47ad-8cd9-0a5c52f58177"
    REGISTRATION_URL = 'https://id.rambler.ru/login-20/mail-registration'
    IMAP_URL = 'https://mail.rambler.ru/settings/mailapps'

    def __init__(self, proxy: Proxy = None, headless: bool = True):
        self._playwright: AsyncPlaywright | None = None
        self._browser: Browser | None = None
        self._proxy = proxy
        self._headless = headless

    async def create_browser(self):
        self._playwright = await async_playwright().start()
        proxy_settings = ProxySettings(
            server=f"{self._proxy.protocol}://{self._proxy.host}:{self._proxy.port}",
            username=self._proxy.login,
            password=self._proxy.password,
        ) if self._proxy else None
        self._browser = await self._playwright.chromium.launch(headless=self._headless, proxy=proxy_settings)

    async def __aenter__(self):
        await self.create_browser()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._browser.close()
        await self._playwright.stop()

    @staticmethod
    async def _set_captcha_token(page: Page, captcha_token: str):
        frame = await page.wait_for_selector('iframe[data-hcaptcha-widget-id]')
        await page.evaluate(
            'args => args[0].setAttribute("data-hcaptcha-response", args[1])',
            [frame, captcha_token],
        )
        await page.evaluate(
            'args => document.querySelector(args[0]).value = args[1]',
            ['textarea[name=h-captcha-response]', captcha_token],
        )
        await page.evaluate('code => hcaptcha.submit(code)', captcha_token)
        await page.wait_for_timeout(500)

    async def _activate_imap(
            self,
            context: BrowserContext,
            captcha_token: str,
            account: RamblerAccount,
    ):
        try:
            # Новая вкладка
            page = await context.new_page()
            await page.goto(self.IMAP_URL)

            # Закрываем попап-сообщение
            popup = await page.wait_for_selector('.rui-Popup-close')
            await popup.click()

            # Активируем IMAP
            await page.get_by_role('button', name='Вкл').click()
            await page.goto('https://mail.rambler.ru/settings/mailapps/change')

            # Решаем капчу
            await self._set_captcha_token(page, captcha_token)

            # Подтверждаем активацию IMAP
            await page.get_by_role('button', name='Отправить').click()

            # Зачем-то ждем полсекунды
            await page.wait_for_timeout(500)

            account.imap_is_activated = True
        except PlaywrightTimeoutError as e:
            logger.error(f"{account} Failed to activate IMAP")
            return

    async def _register(
            self,
            context: BrowserContext,
            captcha_token: str,
            account: RamblerAccount,
    ):
        try:
            # Новая вкладка
            page = await context.new_page()
            url = 'https://id.rambler.ru/login-20/mail-registration'
            await page.goto(url)
            await page.wait_for_timeout(1000)

            # Форма с полями для ввода данных
            form = page.locator('form')

            # Переключаем тип верификации на секретный вопрос
            radio_button = form.locator('//*[@data-cerber-id="registration_form::mail::step_1::verification_type::question"]')
            if await radio_button.is_visible():
                await radio_button.click()

            # Ввод логина и выбор домена
            await form.locator('input[id=login]').type(account.login)
            await form.locator('input[value="@rambler.ru"]').click()
            await form.get_by_text(account.domain).click()

            # Ввод пароля reg_new_password reg_confirm_password
            await form.locator('input[id=newPassword]').type(account.password)
            await form.locator('input[id=confirmPassword]').type(account.password)

            # Выбор и ввод секретного вопроса
            await form.locator('//section[4]/div/div/div/div/div/div/input').click()
            await form.get_by_text("Кличка домашнего животного").click()
            await form.locator('input[id=answer]').type(account.secret)

            # Решаем капчу
            await self._set_captcha_token(page, captcha_token)

            await page.click('button[type=submit]')

            account.registration_datetime = datetime.now()
        except PlaywrightTimeoutError as e:
            logger.error(f"{account} Failed to register account")
            return

        try:
            # Ввод имени и фамилии
            await page.locator("#firstname").type(account.firstname)
            await page.locator("#lastname").type(account.lastname)

            # Выбор пола
            await page.locator('#gender').click()
            await page.get_by_text(GENDER_TO_PLACEHOLDER[account.gender]).click()

            if await page.get_by_placeholder('День').is_visible():
                # Ввод дня рождения
                await page.get_by_placeholder('День').click()
                await page.get_by_text(str(account.birthday.day), exact=True).click()

                # Ввод месяца рождения
                await page.get_by_placeholder("Месяц").click()
                await page.get_by_text(MONTH_NUMBER_TO_PLACEHOLDER[account.birthday.month], exact=True).click()

                # Ввод года рождения
                await page.get_by_placeholder("Год").click()
                await page.get_by_text(str(account.birthday.year), exact=True).click()
            else:
                birthday_calendar = form.locator('#birthday')
                birthday_str = f"{account.birthday.year}-{account.birthday.month:02d}-{account.birthday.day:02d}"
                await birthday_calendar.fill(birthday_str)

            # Отправка формы
            await page.click("button[type=submit]")
            await page.wait_for_timeout(500)

            account.additional_info_is_registered = True
        except PlaywrightTimeoutError as e:
            logger.warning(f"{account} Failed to register additional info (name, gender, birthday)")

    async def register(
            self,
            account: RamblerAccount,
            anticaptcha: AnticaptchaClient,
            *,
            proxy: Proxy = None,
            activate_imap: bool = False,
    ):
        if account.is_registered:
            logger.info(f'Account {account} is already registered')
            return

        proxy_settings = ProxySettings(
            server=f"{proxy.protocol}://{proxy.host}:{proxy.port}",
            username=proxy.login,
            password=proxy.password,
        ) if proxy else None
        context = await self._browser.new_context(proxy=proxy_settings, user_agent=account.useragent)

        await context.add_init_script(path=HCAPTCHA_SCRIPT_FILE_PATH)  # Скрипт для решения hCaptcha

        logger.info(f"{account} Solving captcha...")
        captcha_token = await anticaptcha.hcaptcha(
            self.REGISTRATION_URL,
            self.REGISTRATION_HCAPTCHA_SITE_KEY,
            proxy=proxy.as_url if proxy else None,
            useragent=account.useragent,
        )
        await self._register(context, captcha_token, account)

        if account.is_registered:
            logger.success(f"{account} Account successfully registered")
        else:
            return

        # Активация IMAP
        if activate_imap:
            logger.info(f"{account} Solving captcha...")
            captcha_token = await anticaptcha.hcaptcha(
                self.IMAP_URL,
                self.IMAP_HCAPTCHA_SITE_KEY,
                proxy=proxy.as_url if proxy else None,
                useragent=account.useragent,
            )
            await self._activate_imap(context, captcha_token, account)

            if account.imap_is_activated:
                logger.success(f"{account} IMAP successfully activated")

        await context.close()
