import json

from prettytable import PrettyTable

from utlis import stats


def CN_uid_query(uid, server):
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
    if inn == "Y" or inn == "y" or inn == "":
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


def OS_uid_query(uid, server):
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
    if inn == "Y" or inn == "y" or inn == "":
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


def CN_MiYouSheID_query(MiYouSheID):
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
    if inn == "Y" or inn == "y" or inn == "":
        CN_uid_query(uid=data['game_role_id'], server=data['region'])


def OS_HoYoLabID_query(HoYoLabID):
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
    if inn == "Y" or inn == "y" or inn == "":
        OS_uid_query(uid=data['game_role_id'], server=data['region'])
