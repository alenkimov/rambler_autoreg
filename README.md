# Rambler Autoreg
Python script for automatic mail registration on rambler.
_Ниже есть инструкция на русском._

## Installation and Running on Windows
1. Install [Python 3.11](https://www.python.org/downloads/windows/), checking "Add Python to PATH".
2. Install [Poetry](https://python-poetry.org/docs/).
3. [Download](https://github.com/AlenKimov/rambler_autoreg/archive/refs/heads/main.zip) and unzip the rambler_autoreg repository.
4. Run `install.bat`: this will install all the required libraries.
5. Run `start.bat` to start the script. It'll create settings folder.

## Settings
The script settings are located in the `./settings` folder. Run `start.bat` once to create the settings folder.

The basic settings are contained in `settings.toml`:

```toml
# -- Main settings --
# Count of accounts to register
#   1 <= count <= 1000
count = 1
# Anti-Captcha Service
#   Could be one of the following:
#   "ruCaptcha" and "AntiCaptcha"
#   (Absents by default. 
#    This means that a random service will be selected if API keys have been added)
service = "AntiCaptcha"

# -- Registration --
# Login (before @)
#   Between 8 and 32 Latin letters, numbers, or symbols «._-».
#   Must begin and end with a letter or number.
#   No two identical special symbols may be used in a row.
#   (Absents by default. This means that a random field will be generated for each account)
login = "my_login"
# Password
#   The password must contain from 8 to 32 characters, 
#   include at least one uppercase Latin letter, 
#   one lowercase letter, and one number.
#   You can use these characters: ! @ $ % ^ & * ( ) _ - +
#   (Absents by default. This means that a random field will be generated for each account)
password = "Passw0rd"
# Security code
#   (Absents by default. This means that a random field will be generated for each account)
secret = "my_secret_answer"
# Mail domain
#   Could be one of the following:
#   "@autorambler.ru", "@lenta.ru", "@myrambler.ru", "@rambler.ru", "@rambler.ua", "@ro.ru"
domain = "@rambler.ru"
# Activate IMAP
imap = true

# -- Output --
# Add the write time to the file name
#   Warning! If false, the file will NOT change its name, 
#   which will cause all the data in it to be overwritten when the script is run again!
add_date = true

# -- Debug --
# Logger debug
#   If true, the console will display additional information
debug = false
# Run browser in headed mode
#   The script works through browser emulation.
#   By default, the browser runs in the background (headless mode).
#   If true, the browser will start in the mode and you will see everything the script does.
headed = false
```

API keys for captcha-solving services are set in the `api_keys.toml` file:

```toml
ruCaptcha = 'api_key'
AntiCaptcha = 'api_key'
```

## Запуск под Windows
- Установите [Python 3.11](https://www.python.org/downloads/windows/). Не забудьте поставить галочку напротив "Add Python to PATH".
- Установите пакетный менеджер [Poetry](https://python-poetry.org/docs/).
- Установите [git](https://git-scm.com/download/win).
- С помощью командной строки склонируйте этот репозиторий, после чего перейдите в него:
```bash
git clone https://github.com/AlenKimov/rambler_autoreg.git
cd rambler_autoreg
```
- Установите требуемые библиотеки с помощью Poetry и запустите бота:
```bash
poetry update
poetry run playwright install
poetry run python start.py
```

## Настройки
Настройки скрипта находятся в папке `./settings`.

Основные настройки содержаться в `settings.toml`:

```toml
# -- Основные настройки --
# Количество аккаунтов на регистрацию
#   Стоит искуственное ограничение: 1 <= count <= 1000
count = 1
# Сервис антикапчи
#   Может быть одним из следующих:
#   "ruCaptcha" and "AntiCaptcha"
#   (По умолчанию отсутсвует. Это значит, что будет выбран случайн сервис, 
#    если были добавлены API ключи)
service = "AntiCaptcha"

# -- Тонкости регистрации --
# Поля авторизации
#   От 8 до 32 латинских букв, цифр, или символов «._-».
#   Должен начинаться и заканчиваться на букву или цифру.
#   Нельзя использовать подряд два одинаковых спецсимвола.
#   (По умолчанию отсутсвует. Это значит, что будут сгенерированы случайные поля для каждого аккаунта)
login = "my_login"
#   Пароль должен содержать от 8 до 32 символов, 
#   включать хотя бы одну заглавную латинскую букву, одну строчную и одну цифру.
#   Можно использовать символы ! @ $ % ^ & * ( ) _ - +
password = "Passw0rd"
secret = "my_secret_answer"
# Почтовый домен
#   Может быть одним из следующих:
#   "@autorambler.ru", "@lenta.ru", "@myrambler.ru", "@rambler.ru", "@rambler.ua", "@ro.ru"
domain = "@rambler.ru"
# Активировать IMAP?
imap = true

# -- Настройки вывода --
# Добавлять время записи в название файла?
#   Внимание! При отключении этой функции файл НЕ будет менять название, что приведет к тому,
#   что все данные в нем при повторном запуске скрипта будут перезаписаны!
add_date = true

# -- Настройки отладки --
# Дебаг логера
#   При включенном флаге в консоль будет выводиться дополнительная информация
debug = false
# Запускать в headed режиме браузера?
#   Скрипт работает через эмуляцию браузера.
#   По умолчанию браузер работает в фоне (headless режим).
#   При включенном флаге браузер будет запускаться в headed режиме 
#   и вы будете видеть все, что делает скрипт
headed = false
```

API ключи для сервисов решения капчи задаются в файле `api_keys.toml`:

```toml
ruCaptcha = 'api_key'
AntiCaptcha = 'api_key'
```

API ключи можно взять здесь:
- ruCaptcha: https://rucaptcha.com/enterpage
- AntiCaptcha: https://anti-captcha.com/clients/settings/apisetup

## Output
The script writes the output data to files in the `./output` folder.

## Credits
- [hurek](https://github.com/hurek)/**[mail_farmer](https://github.com/hurek/mail_farmer)**
- [NightStrang6r](https://github.com/NightStrang6r)/**[RamblerAutoReg](https://github.com/NightStrang6r/RamblerAutoReg)**

## Did you like the app?
Rate this repository by putting a star in the upper right corner of the page on GitHub (you need to be logged into 
your account). This gives me motivation to develop this project.

## Contacts
If you have any questions, I will be glad to answer.
- [My personal Telegram account](https://t.me/AlenKimov)
- [My Telegram сhannel](https://t.me/Cum_Insider)