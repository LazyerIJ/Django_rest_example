import hmac
import base64
import hashlib
from api.const import NOT_EXISTS_PHONE_NUMBER, NOT_EXISTS_NAME
import versions


def make_sms_signature(string, secret_key):
    string = bytes(string, 'UTF-8')
    string_hmac = hmac.new(secret_key, string, digestmod=hashlib.sha256).digest()
    string_base64 = base64.b64encode(string_hmac).decode('UTF-8')
    return string_base64


def get_logger_msg_from_ably_error(error, phone_number):
    return f"[{versions.__version__: <5}][{phone_number: <11}][{error.info.code: <6}]{error.detail}"
