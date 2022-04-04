import json

import main
import utlis.DS
import utlis.request

OS_TAKUMI_URL = "https://bbs-api-os.hoyolab.com/"
CN_TAKUMI_URL = "https://api-takumi-record.mihoyo.com/"
OS_GAME_RECORD_URL = "https://bbs-api-os.hoyolab.com/game_record/genshin/api/"
CN_GAME_RECORD_URL = "https://api-takumi-record.mihoyo.com/game_record/app/"
OS_UA = "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
CN_UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBS/2.11.1"


class OS:
    def getUserInfo(HoYoLabID: str) -> {}:
        headers = {
            'User-Agent': OS_UA,
            'x-rpc-client_type': '5',
            'x-rpc-app_version': '1.5.0',
            # 'DS': utlis.DS.generate_ds(),
            'Referer': 'https://webstatic-sea.hoyolab.com/',
            'Cookie': main.Oversea_Cookie
        }
        re = utlis.request.doGet(url=(OS_TAKUMI_URL + "game_record/card/wapi/getGameRecordCard?uid=" + HoYoLabID),
                                 headers=headers)
        nickname = ""
        gameRoleID = ""
        region = ""
        regionName = ""
        level = ""
        if re.status_code == 200:
            js = json.loads(re.text)
            if js['retcode'] == 0:
                msg = js['message']
                if js['data']['list']:
                    js = js['data']['list'][0]
                    nickname = js['nickname']
                    gameRoleID = js["game_role_id"]
                    region = js['region']
                    regionName = js['region_name']
                    level = str(js['level'])
            return json.dumps({"message": msg,
                               "name": nickname,
                               "game_role_id": gameRoleID,
                               "region": region,
                               "region_name": regionName,
                               "level": level})
        return json.dumps({"message": 'http request failed,code: ' + str(re.status_code),
                           "name": nickname,
                           "game_role_id": gameRoleID,
                           "region": region,
                           "region_name": regionName,
                           "level": level})

    def getRoleInfo(UID: str, region: str) -> []:
        headers = {
            'User-Agent': OS_UA,
            'x-rpc-client_type': '4',
            'x-rpc-app_version': '1.5.0',
            'DS': utlis.DS.generate_ds(),
            'Cookie': main.Oversea_Cookie
        }
        re = utlis.request.doGet(url=(OS_GAME_RECORD_URL + "index?role_id=" + UID + "&server=" + region),
                                 headers=headers)
        js = json.loads(re.text)
        card = []
        if js['retcode'] == 0:
            a = js['data']['avatars']
            for b in range(0, len(a) - 1):
                c = {'name': a[b]['name'],
                     'element': a[b]['element'],
                     'fetter': a[b]['fetter'],
                     'level': a[b]['level'],
                     'rarity': a[b]['rarity'],
                     'actived_constellation_num': a[b]['actived_constellation_num']}
                card.append(c)
        return card

    def getGameInfo(UID: str, region: str) -> {}:
        headers = {
            'User-Agent': OS_UA,
            'x-rpc-client_type': '4',
            'x-rpc-app_version': '1.5.0',
            'DS': utlis.DS.generate_ds(),
            'Cookie': main.Oversea_Cookie
        }
        re = utlis.request.doGet(url=(OS_GAME_RECORD_URL + "index?role_id=" + UID + "&server=" + region),
                                 headers=headers)
        js = json.loads(re.text)
        summary = {}
        worldExploration = []
        sereniteaPot = []
        if js['retcode'] == 0:
            a = js['data']['stats']
            summary = {'anemoculus_number': a['anemoculus_number'],
                       'geoculus_number': a['geoculus_number'],
                       'electroculus_number': a['electroculus_number'],
                       'way_point_number': a['way_point_number'],
                       'domain_number': a['domain_number'],
                       'precious_chest_number': a['precious_chest_number'],
                       'exquisite_chest_number': a['exquisite_chest_number'],
                       'luxurious_chest_number': a['luxurious_chest_number'],
                       'common_chest_number': a['common_chest_number'],
                       'magic_chest_number': a['magic_chest_number'],
                       'active_days': a['active_day_number'],
                       'achievement_number': a['achievement_number'],
                       'avatar_number': a['avatar_number'],
                       'spiral_abyss': a['spiral_abyss']}
            b = js['data']['world_explorations']
            for a in b:
                offeringName = ''
                offeringLevel = ''
                if a['offerings']:
                    offeringName = a['offerings'][0]['name']
                    offeringLevel = a['offerings'][0]['level']
                worldExploration.append({'world': a['name'],
                                         'level': a['level'],
                                         'exp': str(a['exploration_percentage'] / 10) + "%",
                                         'offering_name': offeringName,
                                         'offering_level': offeringLevel})
            b = js['data']['homes']
            for a in b:
                sereniteaPot.append({'name': a['name'],
                                     "level": a['level'],
                                     "comfort_num": a['comfort_num'],
                                     'item_num': a['item_num'],
                                     'visit_num': a['visit_num']})
        return json.dumps({'message': js['message'],
                           'summary': summary,
                           'world_exploration': worldExploration,
                           'homes': sereniteaPot})


class CN:
    def getUserInfo(MiYouSheID: str) -> {}:
        headers = {
            'User-Agent': CN_UA,
            'x-rpc-client_type': '5',
            'x-rpc-app_version': '2.11.1',
            'DS': utlis.DS.generate_cn_ds(query={'uid': MiYouSheID}),
            'Cookie': main.CN_Cookie
        }
        re = utlis.request.doGet(url=(CN_TAKUMI_URL + "game_record/app/card/wapi/getGameRecordCard?uid=" + MiYouSheID),
                                 headers=headers)
        js = json.loads(re.text)
        nickname = ""
        gameRoleID = ""
        region = ""
        regionName = ""
        level = ""
        if js['retcode'] == 0:
            if js['data']['list']:
                js = js['data']['list'][0]
                nickname = js['nickname']
                gameRoleID = js["game_role_id"]
                region = js['region']
                regionName = js['region_name']
                level = str(js['level'])
        return json.dumps({"message": js['message'],
                           "name": nickname,
                           "game_role_id": gameRoleID,
                           "region": region,
                           "region_name": regionName,
                           "level": level})

    def getRoleInfo(UID: str, region: str) -> []:
        headers = {
            'User-Agent': CN_UA,
            'x-rpc-client_type': '5',
            'x-rpc-app_version': '2.11.1',
            'DS': utlis.DS.generate_cn_ds(query={"role_id": UID, 'server': region}),
            'Cookie': main.CN_Cookie
        }
        re = utlis.request.doGet(url=(CN_GAME_RECORD_URL + "genshin/api/index?role_id=" + UID + "&server=" + region),
                                 headers=headers)
        js = json.loads(re.text)
        card = []
        if js['retcode'] == 0:
            a = js['data']['avatars']
            for b in range(0, len(a) - 1):
                c = {'name': a[b]['name'],
                     'element': a[b]['element'],
                     'fetter': a[b]['fetter'],
                     'level': a[b]['level'],
                     'rarity': a[b]['rarity'],
                     'actived_constellation_num': a[b]['actived_constellation_num']}
                card.append(c)
        return card

    def getGameInfo(UID: str, region: str) -> {}:
        headers = {
            'User-Agent': CN_UA,
            'x-rpc-client_type': '5',
            'x-rpc-app_version': '2.11.1',
            'DS': utlis.DS.generate_cn_ds(query={"role_id": UID, 'server': region}),
            'Cookie': main.CN_Cookie
        }
        re = utlis.request.doGet(url=(CN_GAME_RECORD_URL + "genshin/api/index?role_id=" + UID + "&server=" + region),
                                 headers=headers)
        js = json.loads(re.text)
        summary = {}
        worldExploration = []
        sereniteaPot = []
        if js['retcode'] == 0:
            a = js['data']['stats']
            summary = {'anemoculus_number': a['anemoculus_number'],
                       'geoculus_number': a['geoculus_number'],
                       'electroculus_number': a['electroculus_number'],
                       'way_point_number': a['way_point_number'],
                       'domain_number': a['domain_number'],
                       'precious_chest_number': a['precious_chest_number'],
                       'exquisite_chest_number': a['exquisite_chest_number'],
                       'luxurious_chest_number': a['luxurious_chest_number'],
                       'common_chest_number': a['common_chest_number'],
                       'magic_chest_number': a['magic_chest_number'],
                       'active_days': a['active_day_number'],
                       'achievement_number': a['achievement_number'],
                       'avatar_number': a['avatar_number'],
                       'spiral_abyss': a['spiral_abyss']}
            b = js['data']['world_explorations']
            for a in b:
                offeringName = ''
                offeringLevel = ''
                if a['offerings']:
                    offeringName = a['offerings'][0]['name']
                    offeringLevel = a['offerings'][0]['level']
                worldExploration.append({'world': a['name'],
                                         'level': a['level'],
                                         'exp': str(a['exploration_percentage'] / 10) + "%",
                                         'offering_name': offeringName,
                                         'offering_level': offeringLevel})
            b = js['data']['homes']
            for a in b:
                sereniteaPot.append({'name': a['name'],
                                     "level": a['level'],
                                     "comfort_num": a['comfort_num'],
                                     'item_num': a['item_num'],
                                     'visit_num': a['visit_num']})
        return json.dumps({'message': js['message'],
                           'summary': summary,
                           'world_exploration': worldExploration,
                           'homes': sereniteaPot})
