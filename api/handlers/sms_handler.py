import time
import requests
from config.utils import get_secret_value
from api.utils import make_sms_signature


class NaverSMSHandler:
    def __init__(self, phone_number, auth_number):
        self.phone_number = phone_number
        self.auth_number = auth_number

    def send_sms(self):
        service_id = get_secret_value("service_id")
        url = 'https://sens.apigw.ntruss.com'
        uri = '/sms/v2/services/' + service_id + '/messages'
        api_url = url + uri
        res = requests.post(url=api_url, json=self._get_body(self.phone_number), headers=self._get_header(uri))
        return res

    def _get_body(self, phone_number):
        body = {
            "type": "SMS",
            "contentType": "COMM",
            "from": get_secret_value("phone_number"),
            "content": "[테스트서버 인증] 안녕하세요. 테스트 서버 회원등록 서비스입니다. [{}]를 입력해주세요.".format(self.auth_number),
            "messages": [{"to": phone_number}]
        }
        return body

    def _get_header(self, uri):
        timeStamp = str(int(time.time() * 1000))
        access_key = get_secret_value("access_key")
        string_to_sign = "POST " + uri + "\n" + timeStamp + "\n" + access_key
        secret_key = bytes(get_secret_value("secret_key"), 'UTF-8')
        signature = make_sms_signature(string_to_sign, secret_key)
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "x-ncp-apigw-timestamp": timeStamp,
            "x-ncp-iam-access-key": access_key,
            "x-ncp-apigw-signature-v2": signature
        }
        return headers

