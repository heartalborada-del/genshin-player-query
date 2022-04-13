import json
import os
import time

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
    with open("options.json", "w") as f:
        f.write(json.dumps({'CN_Cookie': main.CN_Cookie,
                            'Oversea_Cookie': main.Oversea_Cookie,
                            'httpProxy': main.httpProxy}))


def readOptions():
    if not os.path.isfile("options.json"):
        writeOptions()
    with open("options.json", "r") as f:
        data = f.read()
        j = json.loads(data)
        main.CN_Cookie = j['CN_Cookie']
        main.Oversea_Cookie = j['Oversea_Cookie']
        main.httpProxy = j['httpProxy']
        if not main.httpProxy == "":
            print("注意,你当前的代理已设置为: " + main.httpProxy)

