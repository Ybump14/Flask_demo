import base64
import hashlib
import json
import time

import numpy as np
from Crypto.Cipher import AES


def request_headers():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; LCTE; rv:11.0) like Gecko",
        "Platform": "PC",
        "Timestamp": str(round(time.time() * 1000)),
        "Accept-Language": "zh-CN",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "text/plain",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }
    # url = "http://192.168.1.110:4200"
    url = "https://oamng.yuanruiteam.com"
    # url = "https://test-oamng.yuanruiteam.com"
    return {
        "headers": headers,
        "url": url
    }


def pwd_encode(password):
    password = hashlib.sha1(password.encode('utf-8'))
    password = password.hexdigest()
    index = 0
    value = []
    while index < len(password):
        value.append(int(password[index:index + 2], 16))
        index += 2
    value = np.array(value, dtype='uint8')
    value = base64.b64encode(value)
    value = str(value, encoding='utf-8')
    return value


def decode(key, data):
    cipher = AES.new(key)
    result2 = base64.b64decode(data)
    response = cipher.decrypt(result2)
    response = response.decode('utf-8', 'ignore')
    response = response.rstrip('\x01'). \
        rstrip('\x02').rstrip('\x03').rstrip('\x04'). \
        rstrip('\x05').rstrip('\x06').rstrip('\x07'). \
        rstrip('\x08').rstrip('\x09').rstrip('\x10'). \
        rstrip('\x0A').rstrip('\x0B').rstrip('\x0C'). \
        rstrip('\x0D').rstrip('\x0E').rstrip('\x0F'). \
        rstrip('\n').rstrip('\t').rstrip('\r')
    return response


def get_response(data):
    response = data
    if "randomId" in data:
        response = json.loads(decode(data["randomId"], data["encryptData"]))
    return response
