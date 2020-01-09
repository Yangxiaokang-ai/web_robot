import json
import re
import time

import app
from config2 import replySavePath, g5_savePath, sourceSavePath
from ext import db, bot
from model import Questions, User, ReplyLog, MessageLog
import requests

from pyhanlp import *

# 群里保存文件地址
# sourceSavePath =  os.sep.join(["E:", "ReceiveFile"])
from sqlalchemy import or_, desc

r1 = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'

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
        result = User.query.filter(User.trueName.like("%" + name + "%")).all()
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
        result = User.query.filter(
            or_(User.deptName2.like("%" + dept + "%"), User.deptName.like("%" + dept + "%"))).all()
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
        result = User.query.filter(
            or_(User.deptName2.like("%" + dept + "%"), User.deptName.like("%" + dept + "%")),
            User.trueName.like("%" + name + "%")).all()
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


def removePunctuation(key):
    strings = re.sub(r1, "", key).strip()
    return strings


def getAnswerFromData(text):
    result = None
    try:
        result = Questions.query.filter(Questions.keywords.like("%" + text + "%")).first()
        return result
    except Exception as e:
        print(e)
        return result


def insertReplyLog(msg):
    replyLog = ReplyLog()
    replyLog.msg_type = msg.type
    replyLog.message_createtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    if msg.type == 'Text':
        if "日报" in msg.text:
            replyLog.content = msg.text
            db.session.add(replyLog)
            db.session.commit()
            return "小助手将会准时发送"
    else:
        if mkdir(os.sep.join([replySavePath, msg.type])):
            save_path = os.sep.join([replySavePath, msg.type, msg.file_name])
            replyLog.content = save_path
            try:
                if msg.type == "Picture":
                    msg.get_file(save_path)
                    db.session.add(replyLog)
                    db.session.commit()
                    return "小助手将会准时发送"
                else:
                    msg.forward(test)
                    db.session.add(replyLog)
                    db.session.commit()
                    return "小助手转发成功"
            except Exception as e:
                print(e)
                return "暂不支持"


def save5g(msg):
    if msg.type == "Attachment":
        if mkdir(os.sep.join([g5_savePath, msg.type])):
            save_path = os.sep.join([g5_savePath, msg.type, msg.file_name])
            try:
                msg.get_file(save_path)
                questions = Questions.query.get(8)
                questions.answer = save_path
                db.session.add(questions)
                db.session.commit()
            except Exception as e:
                print(e)

    else:
        return


def insertIntoLog(msg):
    message_log = MessageLog()
    message_log.message_createtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    message_log.message_type = msg.type
    message_log.message_sender = msg.member.name
    message_log.message_from = msg.sender.name
    if msg.type == 'Text':
        message_log.content = msg.text
        db.session.add(message_log)
        db.session.commit()
    else:
        save_path = os.sep.join([sourceSavePath, msg.type, msg.file_name])
        try:
            msg.get_file(save_path)
            message_log.content = save_path
            db.session.add(message_log)
            db.session.commit()
        except Exception as e:
            print(e)


test = bot.groups().search("测试2")[0]
test2 = bot.groups().search("测试机器人")[0]
zgs = bot.friends().search("张恭硕")[0]
yxk = bot.friends().search("13653971543")[0]
xuk_z = bot.friends().search("赵旭凯")[0]
zwzx = bot.groups().search("智能网络中心")[0]
zb_sf = bot.groups().search("总部及省分OSS2.0")[0]


@bot.register([zgs, yxk])
def reply_daily(msg):
    with app.app.app_context():
        return insertReplyLog(msg)


@bot.register(xuk_z)
def save_5g(msg):
    with app.app.app_context():
        return save5g(msg)


@bot.register([test, zb_sf, zwzx, test2])
def save_message(msg):
    with app.app.app_context():
        if msg.is_at:
            if "\u2005" in msg.text:
                text = msg.text.strip().split("\u2005", 1)[1]
            else:
                text = msg.text.strip().split(" ", 1)[1]
            if msg.type == 'Text':
                if "帮助" in msg.text:
                    return "你可以试试这样问问我，比如:\n维沃的下载地址是?\n沃运维账号怎么申请？\n沃运维自助菜单添加？\n或者跟我闲聊。"
                elif "联系方式" in text or "电话" in text or "邮箱" in text or '手机' in text:
                    return getAddress(text)
                else:
                    question = getAnswerFromData(text)
                    if question:
                        if question.answer_type == 'Images':
                            msg.reply_image(question.answer)
                        elif question.answer_type == 'File':
                            msg.reply_file(question.answer)
                        else:
                            return question.answer
                    else:
                        return get_text_from_robot(text)
        else:
            insertIntoLog(msg)
            return
