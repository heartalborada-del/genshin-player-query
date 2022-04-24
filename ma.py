from prettytable import PrettyTable

import main
import utils.options
import utils.query
import utils.stats

serverMaps = ['cn_gf01', 'cn_qd01', 'os_asia', 'os_euro', 'os_usa', 'os_cht']


def run():
    table = PrettyTable(['序号', '功能'])
    showList = ["退出", "输入米游社Cookies", "输入 HoYoLab Cookies", "查询玩家信息", "获取帮助", "设置http代理"]
    for a in range(0, showList.__len__()):
        if a == 0:
            table.add_row(["任意键", showList[a]])
            continue
        table.add_row([a, showList[a]])
    table.border = True
    table.valign = 'b'
    print(table.get_string())
    inn = input()
    if inn == '1':
        utils.options.setCNCookies()
        run()
    elif inn == '2':
        utils.options.setOverseaCookies()
        run()
    elif inn == '3':
        selectQueryMethod()
        run()
    elif inn == '4':
        print()
        print("Q: 查询国际服玩家时报错\"http request failed,code: 403\"")
        print("A: 目前需要膜♂法上网，然后配置http代理即可")
        print()
        print("Q: 如何获取Cookie")
        print("A: 打开米游社(HoYoLab),按下F12,选中\"console\"(\"控制台\"),在里面输入\"document.cookie\",复制,粘贴到程序内即可(不要复制开头和结尾的\" \' \")")
        print()
        print("Q: 查询玩家时报错\"Please login\"")
        print("A: 重新复制Cookie到程序内")
        input()
        run()
    elif inn == '5':
        utils.options.setHttpProxy()
        run()


def selectQueryMethod():
    table = PrettyTable(['序号', '请选择查询方式'])
    showList = ["退回到上一级", "米游社/HoYoLab ID查询", "UID+服务器查询"]
    for a in range(0, showList.__len__()):
        if a == 0:
            table.add_row(["任意键", showList[a]])
            continue
        table.add_row([a, showList[a]])
    print(table)
    inn = input()
    if inn == '1':
        table = PrettyTable(['序号', '请选择查询方式'])
        showList = ["退回到上一级", "米游社ID查询", "HoYoLab ID查询"]
        for a in range(0, showList.__len__()):
            if a == 0:
                table.add_row(["任意键", showList[a]])
                continue
            table.add_row([a, showList[a]])
        print(table)
        inn = input()
        if inn == '1':
            if main.CN_Cookie == "":
                print('您还未输入米游社Cookies')
                return
            uid = input('请输入米游社ID\n')
            if uid.isdigit():
                utils.query.CN.CN_MiYouSheID_query(uid)
            else:
                print("UID不为整数")
        elif inn == '2':
            if main.Oversea_Cookie == "":
                print('您还未输入 HoYoLab Cookies')
                return
            uid = input('请输入 HoYoLab ID\n')
            if uid.isdigit():
                utils.query.OS.OS_HoYoLabID_query(uid)
            else:
                print("UID不为整数")
    elif inn == '2':
        table = PrettyTable(['序号', '请选择查询服务器'])
        showList = ["退回到上一级", "天空岛(官服)", "世界树(B服)", "亚服(Asia)", "欧服(Europe)", "美服(America)", "港澳台(TW,HK,MO)"]
        for a in range(0, showList.__len__()):
            if a == 0:
                table.add_row(["任意键", showList[a]])
                continue
            table.add_row([a, showList[a]])
        print(table)
        inn = input()
        if inn == '1' or inn == '2':
            if main.CN_Cookie == "":
                print('您还未输入米游社Cookies')
                return
            server = serverMaps[int(inn) - 1]
            uid = input('请输入玩家UID\n')
            if uid.isdigit():
                utils.query.CN.CN_uid_query(uid, server)
            else:
                print("UID不为整数")
        elif inn == '3' or inn == '4' or inn == '5' or inn == '6':
            if main.Oversea_Cookie == "":
                print('您还未输入 HoYoLab Cookies')
                return
            server = serverMaps[int(inn) - 1]
            uid = input('请输入玩家UID\n')
            if uid.isdigit():
                utils.query.OS.OS_uid_query(uid, server)
            else:
                print("UID不为整数")
