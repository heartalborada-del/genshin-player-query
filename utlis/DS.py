import hashlib
import json
import random
import string
import time
from typing import Any, Mapping

OS_DS_SALT = "6cqshh5dhw73bzxn20oexa9k516chk7s"
CN_DS_SALT = "xV8v4Qu54lUKrEYFZkJhB8cuOh9Asafs"


def generate_ds() -> str:
    t = int(time.time())
    r = "".join(random.choices(string.ascii_letters, k=6))
    h = hashlib.md5(f"salt={OS_DS_SALT}&t={t}&r={r}".encode()).hexdigest()
    return f"{t},{r},{h}"


def generate_cn_ds(body: Any = None, query: Mapping[str, Any] = None) -> str:
    '''
    Body: POST请求
    query: GET请求
    '''
    t = int(time.time())
    r = random.randint(100001, 200000)
    b = json.dumps(body) if body else ""
    q = "&".join(f"{k}={v}" for k, v in sorted(query.items())) if query else ""
    h = hashlib.md5(f"salt={CN_DS_SALT}&t={t}&r={r}&b={b}&q={q}".encode()).hexdigest()
    return f"{t},{r},{h}"
