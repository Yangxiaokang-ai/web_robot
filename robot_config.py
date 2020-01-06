import json, model
import requests

from pyhanlp import *
# from app import bot

# 群里保存文件地址
# sourceSavePath = '/home/deployer/ReceiveFile/'
from sqlalchemy import or_

sourceSavePath = os.sep.join(["/home", "deployer", "ReceiveFile"])
sourceSavePath2 = os.sep.join(["/home", "deployer", "ReceiveFile_ZWZX"])

# 转发消息保存文件地址
replySavePath = os.sep.join(["/home", "deployer", "ReplyFile"])

g5_savePath = os.sep.join(["/home", "deployer", "g5_save"])

# bot.self.send_file(os.sep.join(["/home", "deployer", "ReceiveFile", "Answer", "维沃.png"]))

'''
# 获取聊天组配置
def getGroupConfig():
    botConfig = model.BotConfig.query.filter(model.BotConfig.type == 'GROUP')
    groups = list()
    for bot_config in botConfig:
    # groups.append(bot.groups().search(bot_config.name))
    return groups
'''

# 获取朋友配置
'''
def getFriendConfig():
    friendConfig = model.BotConfig.query.filter(model.BotConfig.type == 'FRIEND')
    friends = list()
    for friend_config in friendConfig:
    friends.append(bot.groups().search(friend_config.name))
    return friends
'''


def mkdir(path):
    path = path.strip()
    path = path.rstrip(os.sep)
    isExist = os.path.exists(path)
    if not isExist:
        try:
            os.makedirs(path)
        except Exception as e:
            print(e)
            return False
        return True
    else:
        return True


def get_text_from_robot(msg):
    app_id = "7ff7084f75b980416b329551e3a02f8a"
    secret = "5bbccb4b84e34acbbc61f738db673251"
    url = "https://api.ownthink.com/bot?appid=AppId&user=SECRET&spoken="
    url = url.replace("AppId", app_id).replace("SECRET", secret)
    sess = requests.get(url + msg)
    result = sess.text
    result = json.loads(result)
    return result['data']['info']['text'].replace('小思', '沃i维').replace('你', '您')


def getAddress(msg):
    dept = ""
    name = ""
    msg = msg.upper()
    keywords = HanLP.segment(msg)
    for term in keywords:
        if str(term.nature) == "nt":
            dept = str(term.word)
        if str(term.nature) == "ns":
            name = str(term.word)
    if dept == "":
        result = model.User.query.filter(model.User.trueName.like("%" + name + "%")).all()
        if len(result) > 0:
            if 50 > len(result) > 1:
                users = "你可能要找这些\n"
                for user in result:
                    users += '姓名:{0}\n手机:{1}\n邮箱:{2}\n固话:{3}\n部门:{4}\n父级部门:{5}\n'.format(str(user.trueName),
                                                                                         str(user.mobliePhone),
                                                                                         str(user.email),
                                                                                         str(user.telPhone),
                                                                                         str(user.deptName2),
                                                                                         str(user.deptName))
            elif len(result) == 1:
                return '姓名:{0}\n手机:{1}\n邮箱:{2}\n固话:{3}\n部门:{4}\n父级部门:{5}\n'.format(str(result[0].trueName),
                                                                                   str(result[0].mobliePhone),
                                                                                   str(result[0].email),
                                                                                   str(result[0].telPhone),
                                                                                   str(result[0].deptName2),
                                                                                   str(result[0].deptName))
                print(222)
            else:
                users = "您可能要找这些\n"
                for i in range(0, 50):
                    # 根据索引访问列表元素
                    user = result[i]
                    users += '姓名:{0}\n手机:{1}\n邮箱:{2}\n固话:{3}\n部门:{4}\n父级部门:{5}\n'.format(str(user.trueName),
                                                                                         str(user.mobliePhone),
                                                                                         str(user.email),
                                                                                         str(user.telPhone),
                                                                                         str(user.deptName2),
                                                                                         str(user.deptName))
                return users + "\n对不起您要找的人重名情况太多了,请带上部门名称,我会变得更加准确哦"
        else:
            return "对不起，我们的通讯录里暂时没有这个部门,我们会继续努力的"
    elif name == "":
        result = model.User.query.filter(
            or_(model.User.deptName2.like("%" + dept + "%"), model.User.deptName.like("%" + dept + "%"))).all()
        if len(result) > 0:
            if 50 > len(result) > 1:
                users = "你可能要找这些\n"
                for user in result:
                    users += '姓名:{0}\n手机:{1}\n邮箱:{2}\n固话:{3}\n部门:{4}\n父级部门:{5}\n'.format(str(user.trueName),
                                                                                         str(user.mobliePhone),
                                                                                         str(user.email),
                                                                                         str(user.telPhone),
                                                                                         str(user.deptName2),
                                                                                         str(user.deptName))
            elif len(result) == 1:
                return '姓名:{0}\n手机:{1}\n邮箱:{2}\n固话:{3}\n部门:{4}\n父级部门:{5}\n'.format(str(result[0].trueName),
                                                                                   str(result[0].mobliePhone),
                                                                                   str(result[0].email),
                                                                                   str(result[0].telPhone),
                                                                                   str(result[0].deptName2),
                                                                                   str(result[0].deptName))
            else:
                users = "您可能要找这些\n"
                for i in range(0, 50):
                    # 根据索引访问列表元素
                    user = result[i]
                    users += '姓名:{0}\n手机:{1}\n邮箱:{2}\n固话:{3}\n部门:{4}\n父级部门:{5}\n'.format(str(user.trueName),
                                                                                         str(user.mobliePhone),
                                                                                         str(user.email),
                                                                                         str(user.telPhone),
                                                                                         str(user.deptName2),
                                                                                         str(user.deptName))
                    return users + "\n对不起您要找的人重名情况太多了,请带上部门名称,我会变得更加准确哦"
        else:
            return "对不起，我们的通讯录里暂时没有这个部门,我们会继续努力的"
    else:
        result = model.User.query.filter(
            or_(model.User.deptName2.like("%" + dept + "%"), model.User.deptName.like("%" + dept + "%")),
            model.User.trueName.like("%" + name + "%")).all()
        if len(result) > 0:
            if 50 > len(result) > 1:
                users = "你可能要找这些\n"
                for user in result:
                    users += '姓名:{0}\n手机:{1}\n邮箱:{2}\n固话:{3}\n部门:{4}\n父级部门:{5}\n'.format(str(user.trueName),
                                                                                         str(user.mobliePhone),
                                                                                         str(user.email),
                                                                                         str(user.telPhone),
                                                                                         str(user.deptName2),
                                                                                         str(user.deptName))
            elif len(result) == 1:
                return '姓名:{0}\n手机:{1}\n邮箱:{2}\n固话:{3}\n部门:{4}\n父级部门:{5}\n'.format(str(result[0].trueName),
                                                                                   str(result[0].mobliePhone),
                                                                                   str(result[0].email),
                                                                                   str(result[0].telPhone),
                                                                                   str(result[0].deptName2),
                                                                                   str(result[0].deptName))
            else:
                users = "您可能要找这些\n"
                for i in range(0, 50):
                    # 根据索引访问列表元素
                    user = result[i]
                    users += '姓名:{0}\n手机:{1}\n邮箱:{2}\n固话:{3}\n部门:{4}\n父级部门:{5}\n'.format(str(user.trueName),
                                                                                         str(user.mobliePhone),
                                                                                         str(user.email),
                                                                                         str(user.telPhone),
                                                                                         str(user.deptName2),
                                                                                         str(user.deptName))
                    return users + "\n对不起您要找的人重名情况太多了,请带上部门名称,我会变得更加准确哦"
        else:
            return "对不起，我们的通讯录里暂时没有这个部门,我们会继续努力的"
