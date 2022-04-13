import json

import requests
from requests import Response
from requests.exceptions import ProxyError

import main


def doGet(url, headers) -> str:
    re = ''
    try:
        re = requests.get(url=url, headers=headers, proxies={'http': main.httpProxy, 'https': main.httpProxy}).text
    except ProxyError as c:
        re = json.dumps({
            'retcode': -400,
            'message': 'Proxy error'
        })
    return re


def doPost(url, headers, body) -> str:
    re = ''
    try:
        re = requests.post(url=url, headers=headers, json=body, proxies={'http': main.httpProxy, 'https': main.httpProxy}).text
    except ProxyError as c:
        re = json.dumps({
            'retcode': -400,
            'message': 'Proxy error'
        })
    return re
