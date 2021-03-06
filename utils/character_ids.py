import json
import os

import utils.request
ids = {}

def getName(character_id: int) -> str:
    name = 'id-' + str(character_id)
    if character_id in ids.keys():
        name = ids[str(character_id)]
    return name

def checkNewIDsList() -> None:
    gh_json = json.loads(getNewIDsList())
    if 'retcode' in gh_json.keys():
        print('获取最新id对照表失败'+gh_json['message'])
        if not os.path.isfile("config/characters_ids.json"):
            print('本地没有id表且无法获取云端表,按回车键退出')
            input()
            os._exit(0)
        return
    local_json = {}
    if not os.path.isdir('config'):
        os.makedirs('config')
    if not os.path.isfile("config/characters_ids.json"):
        with open(file="config/characters_ids.json", mode="w", encoding='UTF-8') as f:
            f.write(json.dumps(gh_json,indent=4,sort_keys=True,ensure_ascii=False))
            ids = gh_json['ids']
        return
    with open(file="config/characters_ids.json", mode="r", encoding='UTF-8') as f:
        local_json = json.load(f)
    print('云端最新版本:'+gh_json['version'])
    print('本地最新版本:'+local_json['version'])
    if float(gh_json['version']) > float(local_json['version']):
        with open(file="config/characters_ids.json", mode="w", encoding='UTF-8') as f:
            f.write(json.dumps(gh_json,indent=4,sort_keys=True,ensure_ascii=False))
            ids = gh_json['ids']
        return
    ids = local_json['ids']
    return
    

def getNewIDsList() -> str:
    headers={
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
    }
    return utils.request.doGet(url='https://gh-proxy.heartalborada.workers.dev/https://raw.githubusercontent.com/heartalborada-del/genshin-player-query/master/json/characters_ids.json',
                               headers=headers)
'''
--- 5 stars ---
琴 10000003
迪卢克 10000016
温迪 10000022
可莉
魈 10000026
旅行者 10000007
莫娜 10000041
刻晴 10000042
七七 10000035
钟离 10000030
达达利亚
阿贝多 10000038
甘雨 10000037
神里绫华 10000002
胡桃 10000046
雷电将军 10000052
优菈 10000051
宵宫 10000049
枫原万叶 10000047
八重神子 10000058
珊瑚宫心海 10000054
埃洛伊 10000062
神里绫人 10000066
荒泷一斗 10000057
申鹤 10000063
'''
'''
--- 4 stars ---
北斗 10000024
安柏 10000021
丽莎 10000006
凯亚 10000015
芭芭拉 10000014
雷泽 10000020
行秋 10000025
菲谢尔 10000031
诺艾尔 10000034
班尼特 10000032
重云 10000036
香菱 10000023
凝光 10000027
砂糖 10000043
迪奥娜 10000039
辛焱 10000044
罗莎莉亚 10000045
云堇 10000064
烟绯 10000048
早柚 10000053
五郎 10000055
九条裟罗 10000056
托马 10000050
'''
