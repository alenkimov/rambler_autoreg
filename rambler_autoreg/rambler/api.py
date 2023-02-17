import requests


def email_is_available(email: str) -> bool:
    # if not email.endswith('@rambler.ru'):
    #     email += '@rambler.ru'

    url = 'https://id.rambler.ru/api/v3/legacy/Rambler::Id::login_available'
    payload = {'params': {'target_email': email}}
    headers = {'content-type': 'application/json'}
    response = requests.request('POST', url, json=payload, headers=headers).json()
    return 'result' not in response
