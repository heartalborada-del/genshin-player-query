import json
import time

import main
import utils.DS
import utils.character_ids
import utils.request
from utils import request

OS_TAKUMI_URL = "https://bbs-api-os.hoyolab.com/"
CN_TAKUMI_URL = "https://api-takumi-record.mihoyo.com/"
OS_GAME_RECORD_URL = "https://bbs-api-os.hoyolab.com/game_record/"
CN_GAME_RECORD_URL = "https://api-takumi-record.mihoyo.com/game_record/app/"
OS_UA = "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
CN_UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBS/2.11.1"


class OS:
    @staticmethod
    def getUserInfo(HoYoLabID: str):
        headers = {
            'User-Agent': OS_UA,
            'x-rpc-client_type': '5',
            'x-rpc-app_version': '1.5.0',
            # 'DS': utils.DS.generate_ds(),
            'Referer': 'https://webstatic-sea.hoyolab.com/',
            'Cookie': main.Oversea_Cookie
        }
        re = utils.request.doGet(url=(OS_TAKUMI_URL + "game_record/card/wapi/getGameRecordCard?uid=" + HoYoLabID),
                                 headers=headers)
        js = json.loads(re)
        nickname = ""
        gameRoleID = ""
        region = ""
        regionName = ""
        level = ""
        if js['retcode'] == 0:
            if js['data']['list']:
                for a in js['data']['list']:
                    if not a['game_id'] == 2:
                        continue
                    nickname = a['nickname']
                    gameRoleID = a["game_role_id"]
                    region = a['region']
                    regionName = a['region_name']
                    level = str(a['level'])
        return json.dumps({"message": js['message'],
                           "name": nickname,
                           "game_role_id": gameRoleID,
                           "region": region,
                           "region_name": regionName,
                           "level": level})

    @staticmethod
    def getRoleInfo(UID: str, region: str):
        headers = {
            'User-Agent': OS_UA,
            'x-rpc-client_type': '4',
            'x-rpc-app_version': '1.5.0',
            'DS': utils.DS.generate_ds(),
            'Cookie': main.Oversea_Cookie
        }
        re = utils.request.doGet(url=(OS_GAME_RECORD_URL + "genshin/api/index?role_id=" + UID + "&server=" + region),
                                 headers=headers)
        js = json.loads(re)
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

    @staticmethod
    def getGameInfo(UID: str, region: str):
        headers = {
            'User-Agent': OS_UA,
            'x-rpc-client_type': '4',
            'x-rpc-app_version': '1.5.0',
            'DS': utils.DS.generate_ds(),
            'Cookie': main.Oversea_Cookie
        }
        re = utils.request.doGet(url=(OS_GAME_RECORD_URL + 'genshin/api/index?role_id=' + UID + "&server=" + region),
                                 headers=headers)
        js = json.loads(re)
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
                       'luxurious_chest_number': a['luxurious_chest_number'],
                       'precious_chest_number': a['precious_chest_number'],
                       'exquisite_chest_number': a['exquisite_chest_number'],
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

    @staticmethod
    def getRoleWeaponAndReliquaries(UID: str, region: str):
        headers = {
            'User-Agent': OS_UA,
            'x-rpc-client_type': '4',
            'x-rpc-app_version': '1.5.0',
            'DS': utils.DS.generate_ds(),
            'Cookie': main.Oversea_Cookie
        }
        re = request.doPost(url=(OS_GAME_RECORD_URL + "genshin/api/character"),
                            headers=headers, body={"role_id": UID, "server": region})
        js = json.loads(re)
        roles = []
        if js['retcode'] == 0:
            for a in js['data']['avatars']:
                role = {'name': a['name'],
                        'element': a['element'],
                        'level': a['level'],
                        'rarity': a['rarity'],
                        'actived_constellation_num': a['actived_constellation_num']}
                weapon = {'name': a['weapon']['name'],
                          'rarity': a['weapon']['rarity'],
                          'type': a['weapon']['type_name'],
                          'level': a['weapon']['level'],
                          'promote_level': a['weapon']['promote_level']}
                reliquaries = []
                for b in a['reliquaries']:
                    affixes = []
                    for c in b['set']['affixes']:
                        affixes.append({'effect': c['effect']})
                    reliquaries.append({'name': b['name'],
                                        'rarity': b['rarity'],
                                        'level': b['level'],
                                        'pos': b['pos'],
                                        'affixes': affixes})
                roles.append({'role': role,
                              'weapon': weapon,
                              'reliquaries': reliquaries})
            return {'message': js['message'], 'roles': roles}
        return [js['message']]

    @staticmethod
    def getSpiralAbyss(self, UID: str, region: str, schedule_type: str):
        headers = {
            'User-Agent': OS_UA,
            'x-rpc-client_type': '4',
            'x-rpc-app_version': '1.5.0',
            'DS': utils.DS.generate_ds(),
            'Cookie': main.Oversea_Cookie
        }
        re = utils.request.doGet(
            url=(OS_GAME_RECORD_URL + "genshin/api/spiralAbyss?server=" + region + "&role_id=" + UID +
                 '&schedule_type=' + schedule_type),
            headers=headers)
        js = json.loads(re)
        tm = ''
        mf = ''
        tbt = 0
        twt = 0
        sid = 0
        reveal_rank = []
        defeat_rank = []
        damage_rank = []
        take_damage_rank = []
        normal_skill_rank = []
        energy_skill_rank = []
        if js['retcode'] == 0:
            da = js['data']
            sid = da['schedule_id']
            tm = time.strftime("%Y.%m.%d", (time.localtime(int(da['start_time'])))) + ' - ' + time.strftime(
                "%Y.%m.%d", time.localtime(int(da['end_time'])))
            mf = js['data']['max_floor']
            tbt = js['data']['total_battle_times']
            twt = js['data']['total_win_times']
            for a in da['reveal_rank']:
                reveal_rank.append({"name": utils.character_ids.getName(a['avatar_id']),
                                    'value': a['value'],
                                    'rarity': a['rarity']})
            for a in da['defeat_rank']:
                defeat_rank.append({"name": utils.character_ids.getName(a['avatar_id']),
                                    'value': a['value'],
                                    'rarity': a['rarity']})
            for a in da['damage_rank']:
                damage_rank.append({"name": utils.character_ids.getName(a['avatar_id']),
                                    'value': a['value'],
                                    'rarity': a['rarity']})
            for a in da['take_damage_rank']:
                take_damage_rank.append({"name": utils.character_ids.getName(a['avatar_id']),
                                         'value': a['value'],
                                         'rarity': a['rarity']})
            for a in da['normal_skill_rank']:
                normal_skill_rank.append({"name": utils.character_ids.getName(a['avatar_id']),
                                          'value': a['value'],
                                          'rarity': a['rarity']})
            for a in da['energy_skill_rank']:
                energy_skill_rank.append({"name": utils.character_ids.getName(a['avatar_id']),
                                          'value': a['value'],
                                          'rarity': a['rarity']})
        return {'message': js['message'],
                'id': sid,
                'time': tm,
                'max_floor': mf,
                'total_battle_times': tbt,
                'total_win_times': twt,
                'rank': {'reveal': reveal_rank,
                         'defeat': defeat_rank,
                         'damage': damage_rank,
                         'take_damage': take_damage_rank,
                         'normal_skill': normal_skill_rank,
                         'energy_skill': energy_skill_rank}
                }


class CN:
    @staticmethod
    def getUserInfo(MiYouSheID: str):
        headers = {
            'User-Agent': CN_UA,
            'x-rpc-client_type': '5',
            'x-rpc-app_version': '2.11.1',
            'DS': utils.DS.generate_cn_ds(query={'uid': MiYouSheID}),
            'Cookie': main.CN_Cookie
        }
        re = utils.request.doGet(url=(CN_TAKUMI_URL + "game_record/app/card/wapi/getGameRecordCard?uid=" + MiYouSheID),
                                 headers=headers)
        js = json.loads(re)
        nickname = ""
        gameRoleID = ""
        region = ""
        regionName = ""
        level = ""
        if js['retcode'] == 0:
            if js['data']['list']:
                for a in js['data']['list']:
                    if not a['game_id'] == 2:
                        continue
                    nickname = a['nickname']
                    gameRoleID = a["game_role_id"]
                    region = a['region']
                    regionName = a['region_name']
                    level = str(a['level'])
        return json.dumps({"message": js['message'],
                           "name": nickname,
                           "game_role_id": gameRoleID,
                           "region": region,
                           "region_name": regionName,
                           "level": level})

    @staticmethod
    def getRoleInfo(UID: str, region: str):
        headers = {
            'User-Agent': CN_UA,
            'x-rpc-client_type': '5',
            'x-rpc-app_version': '2.11.1',
            'DS': utils.DS.generate_cn_ds(query={"role_id": UID, 'server': region}),
            'Cookie': main.CN_Cookie
        }
        re = utils.request.doGet(url=(CN_GAME_RECORD_URL + "genshin/api/index?role_id=" + UID + "&server=" + region),
                                 headers=headers)
        # print(re)
        js = json.loads(re)
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

    @staticmethod
    def getGameInfo(UID: str, region: str):
        headers = {
            'User-Agent': CN_UA,
            'x-rpc-client_type': '5',
            'x-rpc-app_version': '2.11.1',
            'DS': utils.DS.generate_cn_ds(query={"role_id": UID, 'server': region}),
            'Cookie': main.CN_Cookie
        }
        re = utils.request.doGet(url=(CN_GAME_RECORD_URL + "genshin/api/index?role_id=" + UID + "&server=" + region),
                                 headers=headers)
        js = json.loads(re)
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
                       'luxurious_chest_number': a['luxurious_chest_number'],
                       'precious_chest_number': a['precious_chest_number'],
                       'exquisite_chest_number': a['exquisite_chest_number'],
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

    @staticmethod
    def getRoleWeaponAndReliquaries(UID: str, region: str):
        headers = {
            'User-Agent': CN_UA,
            'x-rpc-client_type': '5',
            'x-rpc-app_version': '2.11.1',
            'DS': utils.DS.generate_cn_ds(body={"role_id": UID, "server": region}),
            'Cookie': main.CN_Cookie,
            'Referer': "https://webstatic.mihoyo.com/"
        }
        re = request.doPost(url=(CN_GAME_RECORD_URL + "genshin/api/character"),
                            headers=headers, body={"role_id": UID, "server": region})
        js = json.loads(re)
        roles = []
        if js['retcode'] == 0:
            for a in js['data']['avatars']:
                role = {'name': a['name'],
                        'element': a['element'],
                        'level': a['level'],
                        'rarity': a['rarity'],
                        'actived_constellation_num': a['actived_constellation_num']}
                weapon = {'name': a['weapon']['name'],
                          'rarity': a['weapon']['rarity'],
                          'type': a['weapon']['type_name'],
                          'level': a['weapon']['level'],
                          'promote_level': a['weapon']['promote_level']}
                reliquaries = []
                for b in a['reliquaries']:
                    affixes = []
                    for c in b['set']['affixes']:
                        affixes.append({'effect': c['effect']})
                    reliquaries.append({'name': b['name'],
                                        'rarity': b['rarity'],
                                        'level': b['level'],
                                        'pos': b['pos'],
                                        'affixes': affixes})
                roles.append({'role': role,
                              'weapon': weapon,
                              'reliquaries': reliquaries})
            return {'message': js['message'], 'roles': roles}
        return [js['message']]

    @staticmethod
    def getSpiralAbyss(UID: str, region: str, schedule_type: str):
        headers = {
            'User-Agent': CN_UA,
            'x-rpc-client_type': '5',
            'x-rpc-app_version': '2.11.1',
            'DS': utils.DS.generate_cn_ds(query={"role_id": UID, "server": region, 'schedule_type': schedule_type}),
            'Cookie': main.CN_Cookie,
            'Referer': "https://webstatic.mihoyo.com/"
        }
        re = utils.request.doGet(url=(CN_GAME_RECORD_URL + "genshin/api/spiralAbyss?&role_id=" + UID +
                                      '&server=' + region + '&schedule_type=' + schedule_type),
                                 headers=headers)
        js = json.loads(re)
        tm = ''
        mf = ''
        tbt = 0
        twt = 0
        id = 0
        reveal_rank = []
        defeat_rank = []
        damage_rank = []
        take_damage_rank = []
        normal_skill_rank = []
        energy_skill_rank = []
        if js['retcode'] == 0:
            da = js['data']
            id = da['schedule_id']
            tm = time.strftime("%Y.%m.%d", (time.localtime(int(da['start_time'])))) + ' - ' + time.strftime(
                "%Y.%m.%d", time.localtime(int(da['end_time'])))
            mf = js['data']['max_floor']
            tbt = js['data']['total_battle_times']
            twt = js['data']['total_win_times']
            for a in da['reveal_rank']:
                reveal_rank.append({"name": utils.character_ids.getName(a['avatar_id']),
                                    'value': a['value'],
                                    'rarity': a['rarity']})
            for a in da['defeat_rank']:
                defeat_rank.append({"name": utils.character_ids.getName(a['avatar_id']),
                                    'value': a['value'],
                                    'rarity': a['rarity']})
            for a in da['damage_rank']:
                damage_rank.append({"name": utils.character_ids.getName(a['avatar_id']),
                                    'value': a['value'],
                                    'rarity': a['rarity']})
            for a in da['take_damage_rank']:
                take_damage_rank.append({"name": utils.character_ids.getName(a['avatar_id']),
                                         'value': a['value'],
                                         'rarity': a['rarity']})
            for a in da['normal_skill_rank']:
                normal_skill_rank.append({"name": utils.character_ids.getName(a['avatar_id']),
                                          'value': a['value'],
                                          'rarity': a['rarity']})
            for a in da['energy_skill_rank']:
                energy_skill_rank.append({"name": utils.character_ids.getName(a['avatar_id']),
                                          'value': a['value'],
                                          'rarity': a['rarity']})
        return {'message': js['message'],
                'id': id,
                'time': tm,
                'max_floor': mf,
                'total_battle_times': tbt,
                'total_win_times': twt,
                'rank': {'reveal': reveal_rank,
                         'defeat': defeat_rank,
                         'damage': damage_rank,
                         'take_damage': take_damage_rank,
                         'normal_skill': normal_skill_rank,
                         'energy_skill': energy_skill_rank}
                }
