from array import array
import json
from typing import List

from prettytable import PrettyTable

import utils.stats
from utils import stats


class CN:
    @staticmethod
    def CN_uid_query(uid: str, server: str):
        data = json.loads(stats.CN.getGameInfo(uid, server))
        if not data['message'] == 'OK':
            print("获取信息错误 错误信息: " + data['message'])
            return
        table = PrettyTable(['类型', '数据'])
        showList = ["风神曈", "岩神瞳", "雷神瞳",
                    "解锁传送点", '解锁秘境',
                    "华丽宝箱数", '珍贵宝箱数', '精致宝箱数', '普通宝箱数', '奇馈宝箱数',
                    '活跃天数', '成就达成数', '获得角色数', '深境螺旋']
        i = 0
        for key in data['summary']:
            table.add_row([showList[i], data['summary'][key]])
            i += 1
        print(table)
        table = PrettyTable(['地图名称', '探索度', '声望等级', '地区特殊供奉', '供奉等级'])
        for a in data['world_exploration']:
            table.add_row([str(a['world']).replace("·", "-"),
                           a['exp'],
                           a['level'],
                           a['offering_name'] and a['offering_name'] or '---',
                           a['offering_name'] and a['offering_level'] or '---'])
        print(table)
        table = PrettyTable(['尘歌壶地图', '信任等阶', '最高洞天仙力', '获得摆件数', '历史访客数'])
        for a in data['homes']:
            table.add_row([a['name'],
                           a['level'],
                           a['comfort_num'],
                           a['item_num'],
                           a['visit_num']])
        print(table)
        inn = input("是否显示角色\n(Y/n)")
        if inn == "Y" or inn == "y":
            data = stats.CN.getRoleInfo(uid, server)
            table = PrettyTable(['角色名称',
                                 '元素类型',
                                 '好感度等级',
                                 '角色等级',
                                 '稀有度',
                                 '命数'])
            for a in data:
                table.add_row([a['name'],
                               a['element'],
                               a['fetter'],
                               a['level'],
                               a['rarity'],
                               a['actived_constellation_num']])
            print(table)
        inn = input("是否查看角色详情\n(Y/n)")
        if inn == "Y" or inn == "y":
            CN.CN_role_info(uid, server)
        inn = input("是否查看本期与上期深渊数据\n(Y/n)")
        if inn == "Y" or inn == "y":
            CN.CN_spiralAbyss_info(uid, server)

    @staticmethod
    def CN_MiYouSheID_query(MiYouSheID: str):
        data = json.loads(stats.CN.getUserInfo(MiYouSheID))
        if not data['message'] == 'OK':
            print("获取信息错误 错误信息: " + data['message'])
            return
        table = PrettyTable(['类型', '数据'])
        showList = ["玩家名", "UID", "服务器", "服务器名称", '冒险等级']
        b = 0
        for a in data:
            if not b == 0:
                table.add_row([showList[b - 1], data[a]])
            b += 1
        print(table)
        inn = input("继续查询?\n(Y/n)")
        if inn == "Y" or inn == "y":
            CN.CN_uid_query(uid=data['game_role_id'], server=data['region'])

    @staticmethod
    def CN_role_info(uid: str, server: str):
        data = stats.CN.getRoleWeaponAndReliquaries(UID=uid, region=server)
        table1 = PrettyTable(["ID", '角色名称', '等级', '元素类型', '稀有度', '命之座等级'])
        table2 = PrettyTable(["ID", '角色名称', '武器', '武器类型', '稀有度', '武器等级', '精炼等级'])
        table3 = PrettyTable(["ID", '角色名称', '生之花', '死之羽', '时之沙', '空之杯', '理之冠'])
        i = 0
        for role in data['roles']:
            ro = role['role']
            table1.add_row([i, ro['name'], ro['level'], ro['element'], ro['rarity'], ro['actived_constellation_num']])
            wp = role['weapon']
            table2.add_row([i, ro['name'], wp['name'], wp['type'], wp['rarity'], wp['level'], wp['promote_level']])
            ren = ["---", "---", "---", "---", "---"]
            rele = ['', '', '', '', '']
            rer = ['', '', '', '', '']
            for rel in role['reliquaries']:
                ren[rel['pos'] - 1] = rel['name']
                rele[rel['pos'] - 1] = rel['level']
                rer[rel['pos'] - 1] = rel['rarity']
            table3.add_row([i,
                            ro['name'],
                            ren[0] + '-' + str(rele[0]) + '-' + str(rer[0]),
                            ren[1] + '-' + str(rele[1]) + '-' + str(rer[1]),
                            ren[2] + '-' + str(rele[2]) + '-' + str(rer[2]),
                            ren[3] + '-' + str(rele[3]) + '-' + str(rer[3]),
                            ren[4] + '-' + str(rele[4]) + '-' + str(rer[4])])
            i += 1
        inn = input("是否查看角色信息?\n(Y/n)")
        if inn == "Y" or inn == "y":
            print(table1)
        inn = input("是否查看角色装备武器?\n(Y/n)")
        if inn == "Y" or inn == "y":
            print(table2)
        inn = input("是否查看角色装备圣遗物?\n(Y/n)")
        if inn == "Y" or inn == "y":
            print(table3)
            inn = input("是否查看角色圣遗物词条?\n(Y/n)")
            if inn == "Y" or inn == "y":
                reliquaries_info(data)

    @staticmethod
    def CN_spiralAbyss_info(uid: str, server: str):
        data1 = utils.stats.CN.getSpiralAbyss(UID=uid, region=server, schedule_type='1')
        data2 = utils.stats.CN.getSpiralAbyss(UID=uid, region=server, schedule_type='2')
        table = PrettyTable(['期数', '开始-结束时间', '总挑战次数', '胜利次数', '最深抵达'])
        # print(data1)
        table.add_row([data1['id'], data1['time'], data1['total_battle_times'],
                       data1['total_win_times'], data1['max_floor']])
        table.add_row([data2['id'], data2['time'], data2['total_battle_times'],
                       data2['total_win_times'], data2['max_floor']])
        table.hrules = True
        print(table)
        table = PrettyTable(['期数', '出战次数', '最多击破数', '最强一击', '承受最多伤害', '元素战技释放数', '元素爆发次数'])
        rank = utils.query.rank_info(data1['rank'])
        table.add_row([data1['id'], rank[0], rank[1], rank[2], rank[3], rank[4], rank[5]])
        rank = utils.query.rank_info(data2['rank'])
        # print(rank)
        table.add_row([data2['id'], rank[0], rank[1], rank[2], rank[3], rank[4], rank[5]])
        table.hrules = True
        print(table)


class OS:
    @staticmethod
    def OS_uid_query(uid: str, server: str):
        data = json.loads(stats.OS.getGameInfo(uid, server))
        if not data['message'] == 'OK':
            print("获取信息错误 错误信息: " + data['message'])
            return
        table = PrettyTable(['类型', '数据'])
        showList = ["风神曈", "岩神瞳", "雷神瞳",
                    "解锁传送点", '解锁秘境',
                    "华丽宝箱数", '珍贵宝箱数', '精致宝箱数', '普通宝箱数', '奇馈宝箱数',
                    '活跃天数', '成就达成数', '获得角色数', '深境螺旋']
        i = 0
        for key in data['summary']:
            table.add_row([showList[i], data['summary'][key]])
            i += 1
        print(table)
        table = PrettyTable(['地图名称', '探索度', '声望等级', '地区特殊供奉', '供奉等级'])
        for a in data['world_exploration']:
            table.add_row([a['world'],
                           a['exp'],
                           a['level'],
                           a['offering_name'] and a['offering_name'] or '---',
                           a['offering_name'] and a['offering_level'] or '---'])
        print(table)
        table = PrettyTable(['尘歌壶地图', '信任等阶', '最高洞天仙力', '获得摆件数', '历史访客数'])
        for a in data['homes']:
            table.add_row([a['name'],
                           a['level'],
                           a['comfort_num'],
                           a['item_num'],
                           a['visit_num']])
        print(table)
        inn = input("是否显示角色\n(Y/n)")
        if inn == "Y" or inn == "y":
            data = stats.OS.getRoleInfo(uid, server)
            table = PrettyTable(['角色名称',
                                 '元素类型',
                                 '好感度等级',
                                 '角色等级',
                                 '稀有度',
                                 '命数'])
            for a in data:
                table.add_row([a['name'],
                               a['element'],
                               a['fetter'],
                               a['level'],
                               a['rarity'],
                               a['actived_constellation_num']])
            print(table)
        inn = input("是否查看角色详情\n(Y/n)")
        if inn == "Y" or inn == "y":
            OS.OS_role_info(uid, server)
        inn = input("是否查看本期与上期深渊数据\n(Y/n)")
        if inn == "Y" or inn == "y":
            OS.OS_spiralAbyss_info(uid, server)

    @staticmethod
    def OS_HoYoLabID_query(HoYoLabID: str):
        data = json.loads(stats.OS.getUserInfo(HoYoLabID))
        if not data['message'] == 'OK':
            print("获取信息错误 错误信息: " + data['message'])
            return
        table = PrettyTable(['类型', '数据'])
        showList = ["玩家名", "UID", "服务器", "服务器名称", '冒险等级']
        b = 0
        for a in data:
            if not b == 0:
                table.add_row([showList[b - 1], data[a]])
            b += 1
        print(table)
        inn = input("继续查询?\n(Y/n)")
        if inn == "Y" or inn == "y":
            OS.OS_uid_query(uid=data['game_role_id'], server=data['region'])

    @staticmethod
    def OS_role_info(uid: str, server: str):
        data = stats.OS.getRoleWeaponAndReliquaries(region=server)
        table1 = PrettyTable(["ID", '角色名称', '等级', '元素类型', '稀有度', '命之座等级'])
        table2 = PrettyTable(["ID", '角色名称', '武器', '武器类型', '稀有度', '武器等级', '精炼等级'])
        table3 = PrettyTable(["ID", '角色名称', '生之花', '死之羽', '时之沙', '空之杯', '理之冠'])
        i = 0
        for role in data['roles']:
            ro = role['role']
            table1.add_row([i, ro['name'], ro['level'], ro['element'], ro['rarity'], ro['actived_constellation_num']])
            wp = role['weapon']
            table2.add_row([i, ro['name'], wp['name'], wp['type'], wp['rarity'], wp['level'], wp['promote_level']])
            ren = ["---", "---", "---", "---", "---"]
            rele = ['', '', '', '', '']
            rer = ['', '', '', '', '']
            for rel in role['reliquaries']:
                ren[rel['pos'] - 1] = rel['name']
                rele[rel['pos'] - 1] = rel['level']
                rer[rel['pos'] - 1] = rel['rarity']
            table3.add_row([i,
                            ro['name'],
                            ren[0] + '-' + str(rele[0]) + '-' + str(rer[0]),
                            ren[1] + '-' + str(rele[1]) + '-' + str(rer[1]),
                            ren[2] + '-' + str(rele[2]) + '-' + str(rer[2]),
                            ren[3] + '-' + str(rele[3]) + '-' + str(rer[3]),
                            ren[4] + '-' + str(rele[4]) + '-' + str(rer[4])])
            i += 1
        inn = input("是否查看角色信息?\n(Y/n)")
        if inn == "Y" or inn == "y":
            print(table1)
        inn = input("是否查看角色装备武器?\n(Y/n)")
        if inn == "Y" or inn == "y":
            print(table2)
        inn = input("是否查看角色装备圣遗物?\n(Y/n)")
        if inn == "Y" or inn == "y":
            print(table3)
            inn = input("是否查看角色圣遗物词条?\n(Y/n)")
            if inn == "Y" or inn == "y":
                reliquaries_info(data)

    @staticmethod
    def OS_spiralAbyss_info(uid: str, server: str):
        data1 = utils.stats.OS.getSpiralAbyss(UID=uid, region=server, schedule_type='1')
        data2 = utils.stats.OS.getSpiralAbyss(UID=uid, region=server, schedule_type='2')
        table = PrettyTable(['期数', '开始-结束时间', '总挑战次数', '胜利次数', '最深抵达'])
        # print(data1)
        table.add_row([data1['id'], data1['time'], data1['total_battle_times'],
                       data1['total_win_times'], data1['max_floor']])
        table.add_row([data2['id'], data2['time'], data2['total_battle_times'],
                       data2['total_win_times'], data2['max_floor']])
        table.hrules = True
        print(table)
        table = PrettyTable(['期数', '出战次数', '最多击破数', '最强一击', '承受最多伤害', '元素爆发次数', '元素战技释放数'])
        rank = utils.query.rank_info(data1['rank'])
        table.add_row([data1['id'], rank[0], rank[1], rank[2], rank[3], rank[4], rank[5]])
        rank = utils.query.rank_info(data2['rank'])
        table.add_row([data2['id'], rank[0], rank[1], rank[2], rank[3], rank[4], rank[5]])
        table.hrules = True
        print(table)


def reliquaries_info(data: dict):
    inn = input("请输入你要查询的人物id\n")
    if inn.isalnum():
        if int(inn) < 0 or int(inn) > len(data['roles']) - 1:
            reliquaries_info(data)
            return
        table4 = PrettyTable(['角色名称', '圣遗物', '词条'])
        table4.hrules = True
        for a in data['roles'][int(inn)]['reliquaries']:
            aff = ""
            for b in range(0, len(a['affixes'])):
                eff = a['affixes'][b]['effect']
                st2 = str(eff).split("，")
                eff = ''
                for c in st2:
                    eff += c + "\n"
                if b == len(a['affixes']) - 1:
                    aff += '词条' + str(b + 1) + ": " + eff
                    continue
                aff += '词条' + str(b + 1) + ": " + eff
            table4.add_row([data['roles'][int(inn)]['role']['name'], a['name'], aff])
        print(table4)
        inn = input('是否要继续查询\n(Y/n)')
        if inn == "Y" or inn == "y":
            reliquaries_info(data)
        else:
            return
    elif inn == '':
        return
    else:
        print("输入错误,请重新输入,退出直接按回车")
        reliquaries_info(data)
    return


def rank_info(rank: dict) -> list[str]:
    reveal = ''
    defeat = ''
    damage = ''
    take_damage = ''
    normal_skill = ''
    energy_skill = ''
    for a in range(0, len(rank['reveal'])):
        info = rank['reveal'][a]
        if a == len(rank['reveal']) - 1:
            reveal += info['name'] + '-' + str(info['value'])
            continue
        reveal += info['name'] + '-' + str(info['value']) + '\n'
    for a in range(0, len(rank['defeat'])):
        info = rank['defeat'][a]
        if a == len(rank['defeat']) - 1:
            defeat += info['name'] + '-' + str(info['value'])
            continue
        defeat += info['name'] + '-' + str(info['value']) + '\n'
    for a in range(0, len(rank['damage'])):
        info = rank['damage'][a]
        if a == len(rank['damage']) - 1:
            damage += info['name'] + '\n' + str(info['value'])
            continue
        damage += info['name'] + '\n' + str(info['value']) + '\n'
    for a in range(0, len(rank['take_damage'])):
        info = rank['take_damage'][a]
        if a == len(rank['take_damage']) - 1:
            take_damage += info['name'] + '\n' + str(info['value'])
            continue
        take_damage += info['name'] + '\n' + str(info['value']) + '\n'
    for a in range(0, len(rank['normal_skill'])):
        info = rank['normal_skill'][a]
        if a == len(rank['normal_skill']) - 1:
            normal_skill += info['name'] + '-' + str(info['value'])
            continue
        normal_skill += info['name'] + '-' + str(info['value']) + '\n'
    for a in range(0, len(rank['energy_skill'])):
        info = rank['energy_skill'][a]
        if a == len(rank['energy_skill']) - 1:
            energy_skill += info['name'] + '-' + str(info['value'])
            continue
        energy_skill += info['name'] + '-' + str(info['value']) + '\n'
    return [reveal and reveal or '---',
            defeat and defeat or '---',
            damage and damage or '---',
            take_damage and take_damage or '---',
            normal_skill and normal_skill or '---',
            energy_skill and energy_skill or '---']
