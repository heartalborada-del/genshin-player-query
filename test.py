import requests

import json

import utils.character_ids

if __name__ == '__main__':
    print(('https://hoyolab-proxy.heartalborada.workers.dev/https://bbs-api-os.hoyolab.com/').encode().decode(
        "unicode_escape"))
    re = requests.get('https://hoyolab-proxy.heartalborada.workers.dev/https://bbs-api-os.hoyolab.com/',
                      proxies={'http': '', 'https': ''}, headers={"x-real-ip": "24.37.245.42"})
    print(re.text)
