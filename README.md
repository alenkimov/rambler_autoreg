# Rambler Autoreg
[![Telegram channel](https://img.shields.io/endpoint?url=https://runkit.io/damiankrawczyk/telegram-badge/branches/master?url=https://t.me/cum_insider)](https://t.me/cum_insider)

Python script for automatic mail registration on rambler.
Supports `.txt` and `.csv` output formats.

- [Запуск под Windows](#запуск-под-windows)

## Запуск под Windows
- Установите [Python 3.11](https://www.python.org/downloads/windows/). Не забудьте поставить галочку напротив "Add Python to PATH".
- Установите пакетный менеджер [Poetry](https://python-poetry.org/docs/) вручную по [этой инструкции](https://teletype.in/@alenkimov/poetry) или по инструкции с официального сайта.
- Установите [git](https://git-scm.com/download/win). Это позволит с легкостью получать обновления скрипта командой `git pull`
- Откройте консоль в удобном месте...
  - Склонируйте (или [скачайте](https://github.com/alenkimov/rambler_autoreg/archive/refs/heads/main.zip)) этот репозиторий:
    ```bash
    git clone https://github.com/alenkimov/rambler_autoreg
    ```
  - Перейдите в папку проекта:
    ```bash
    cd rambler_autoreg
    ```
  - Установите требуемые зависимости следующей командой или запуском файла `INSTALL.bat`:
    ```bash
    poetry install
    poetry run playwright install
    ```
  - Запустите скрипт следующей командой или запуском файла `START.bat`:
    ```bash
    poetry run python main.py
    ```