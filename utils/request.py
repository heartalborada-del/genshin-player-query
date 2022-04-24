import json

import requests
from requests.exceptions import ProxyError,ConnectionError
import main


def doGet(url, headers) -> str:
    re = ''
    ret = None
    try:
        ret = requests.get(url=url, headers=headers, proxies={'http': main.httpProxy, 'https': main.httpProxy})
    except ProxyError as c:
        re = json.dumps({
            'retcode': -400,
            'message': 'Proxy error'
        })
    except ConnectionError as c:
        re = json.dumps({
            'retcode': -100,
            'message': 'Internet error'
        })
    if not ret.status_code == 200:
        return json.dumps({
            'retcode': ret.status_code,
            'message': 'Request failed'
        })
    re = ret.text
    return re


def doPost(url, headers, body) -> str:
    re = ''
    ret = None
    try:
        ret = requests.post(url=url, headers=headers, json=body, proxies={'http': main.httpProxy, 'https': main.httpProxy})
    except ProxyError as c:
        re = json.dumps({
            'retcode': -400,
            'message': 'Proxy error'
        })
    except ConnectionError as c:
        re = json.dumps({
            'retcode': -100,
            'message': 'Internet error'
        })
    if not ret.status_code == 200:
        return json.dumps({
            'retcode': ret.status_code,
            'message': 'Request failed'
        })
    re = ret.text
    return re
