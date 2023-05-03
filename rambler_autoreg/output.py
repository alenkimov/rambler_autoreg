"""Функция записи данных в файлы"""
from datetime import datetime
import json
import csv

# Third-party libraries
from slugify import slugify

# Libraries of this project
from rambler_autoreg.logger import logger
from rambler_autoreg.paths import OUTPUT_DIR
from rambler_autoreg.rambler.account_model import RamblerAccount


def write_txt(account: RamblerAccount, filename: str = 'accounts'):
    txt_filename = f'{filename}.txt'
    txt_filepath = OUTPUT_DIR / txt_filename
    with open(txt_filepath, 'a', encoding='utf-8') as file:
        email = account.email()
        password = account.password
        secret = account.secret
        file.write(f'{email}:{password}:{secret}\n')
    logger.success(f'Data was successfully written to the file {txt_filename}')


def write_csv(account: RamblerAccount, filename: str = 'accounts'):
    csv_filename = f'{filename}.csv'
    csv_filepath = OUTPUT_DIR / csv_filename
    with open(csv_filepath, mode="a", encoding='utf-8') as file:
        file_writer = csv.writer(file, delimiter=";")
        file_writer.writerow([account.email(), account.password, account.secret])
    logger.success(f'Data was successfully written to the file {csv_filename}')


def write_json(data, filename: str = 'data', *, add_date: bool = True):
    """
    Записывает данные в файл.

    :param data: Данные на запись.
    :param filename: Имя файла. Если обнаружится файл с тем же названием, он будет перезаписан!
    :param add_date: Добавляет дату и время в конец названия файла.
    Если установить значение True, то будет записывать данные в новый файл,
    название которого строится по шаблону "{filename}_{now_datetime}.json".
    """
    logger.info(f'Writing data to a file..')
    if not data:
        logger.warning(f'There is no data to write')
        return

    filename = slugify(filename)
    if add_date:
        now_datetime = f'{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}'
        json_filename = f'{filename}_{now_datetime}.json'
    else:
        json_filename = f'{filename}.json'
    json_filepath = OUTPUT_DIR / json_filename

    with open(json_filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False, default=str)
        # ensure_ascii=False — Для русских символов
        # default=str — Для сериализации datetime.datetime, datetime.date
    logger.success(f'Data was successfully written to the file {json_filename}')
