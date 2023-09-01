import csv
import os

from bot.paths import OUTPUT_DIR
from bot.rambler import RamblerAccount


def write_txt(account: RamblerAccount, filename: str = 'accounts'):
    txt_filename = f'{filename}.txt'
    txt_filepath = OUTPUT_DIR / txt_filename
    with open(txt_filepath, 'a', encoding='utf-8') as file:
        account_data = f':'.join([
            account.email,
            account.password,
            account.secret,
        ])
        file.write(f'{account_data}\n')


# def write_csv(account: RamblerAccount, filename: str = 'accounts', proxy: str = None):
#     csv_filename = f'{filename}.csv'
#     csv_filepath = OUTPUT_DIR / csv_filename
#     with open(csv_filepath, mode="a", encoding='utf-8', newline='') as file:
#         file_writer = csv.writer(file, delimiter=";")
#         row = [
#             account.registration_datetime,
#             account.email,
#             account.password,
#             account.secret,
#             account.imap_is_activated,
#             account.additional_info_is_registered,
#             account.gender,
#             account.firstname,
#             account.lastname,
#             account.useragent,
#         ]
#         if proxy: row.append(proxy)
#         file_writer.writerow(row)

def write_csv(account: RamblerAccount, filename: str = 'accounts', proxy: str = None):
    csv_filename = f'{filename}.csv'
    csv_filepath = OUTPUT_DIR / csv_filename
    headers = [
        "Registration Datetime",
        "Email",
        "Password",
        "Secret",
        "IMAP is Activated",
        "Additional Info is Registered",
        "Gender",
        "First Name",
        "Last Name",
        "User Agent",
        "Proxy",  # Добавляем колонку "Proxy" по умолчанию
    ]

    # Проверка существования файла
    file_exists = os.path.isfile(csv_filepath)

    with open(csv_filepath, mode="a", encoding='utf-8', newline='') as file:
        file_writer = csv.writer(file, delimiter=";")

        # Если файл не существует, добавляем заголовки
        if not file_exists:
            file_writer.writerow(headers)

        row = [
            account.registration_datetime,
            account.email,
            account.password,
            account.secret,
            account.imap_is_activated,
            account.additional_info_is_registered,
            account.gender,
            account.firstname,
            account.lastname,
            account.useragent,
            proxy if proxy else "",
        ]

        file_writer.writerow(row)
