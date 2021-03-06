import json
import os

import main


def setCNCookies():
    main.CN_Cookie = input("请输入你的米游社Cookies\n")
    writeOptions()


def setOverseaCookies():
    main.Oversea_Cookie = input("请输入你的 HoYoLab Cookies\n")
    writeOptions()


def setHttpProxy():
    main.httpProxy = input("请输入你的HTTP代理地址\n")
    writeOptions()


def writeOptions():
    with open(file="config/options.json", mode="w", encoding='utf-8') as f:
        f.write(json.dumps({'CN_Cookie': main.CN_Cookie,
                            'Oversea_Cookie': main.Oversea_Cookie,
                            'httpProxy': main.httpProxy},
                            indent = 4,
                            ensure_ascii=False))


def readOptions():
    if not os.path.isdir('config'):
        os.makedirs('config')
    if not os.path.isfile("config/options.json"):
        writeOptions()
    with open(file="config/options.json", mode="r", encoding='utf-8') as f:
        data = f.read()
        j = json.loads(data)
        main.CN_Cookie = j['CN_Cookie']
        main.Oversea_Cookie = j['Oversea_Cookie']
        main.httpProxy = j['httpProxy']
        if not main.httpProxy == "":
            print("注意,你当前的代理已设置为: " + main.httpProxy)

