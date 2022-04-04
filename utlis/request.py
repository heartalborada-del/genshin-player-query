import requests
from requests import Response

import main


def doGet(url, headers) -> Response:
    re = requests.get(url=url, headers=headers, proxies={'http': main.httpProxy, 'https': main.httpProxy})
    return re
