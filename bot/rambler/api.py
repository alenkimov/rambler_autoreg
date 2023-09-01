from better_automation import BetterHTTPClient


class RamblerAPI(BetterHTTPClient):
    async def login_is_available(self, email: str) -> bool:
        url = 'https://id.rambler.ru/api/v3/legacy/Rambler::Id::login_available'
        payload = {'params': {'target_email': email}}
        response = await self.request('POST', url, json=payload)
        response_json = await response.json()
        return 'result' not in response_json

    # async def activate_imap(self, timestamp_milliseconds: int, captcha_token: str) -> bool:
    #     url = "https://mail.rambler.ru/api/v2"
    #     payload = {
    #         "method": "Rambler::Mail::set_smtp_flags",
    #         "params": [
    #             {
    #                 "smtp_flags": False,
    #                 "captcha_token": captcha_token,
    #                 "captcha_type": "hcaptcha"
    #             }
    #         ],
    #         "id": timestamp_milliseconds,
    #         "rpc": "2.0"
    #     }
    #     response = await self.request("POST", url, json=payload)
    #     response_json = await response.json()
    #     return response_json["result"]["success"]
