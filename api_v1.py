import os

from flask import jsonify, request, Blueprint

import config2
from ext import db, bot
import base64util
from model import SendMessage

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api_v1')


@api_v1.route("/addMessage", methods=['POST'])
def add_message():
    message_type = request.form.get("type")
    message = SendMessage()
    print(request.form)
    print(request.get_json())
    try:
        group = bot.groups().search(request.form.get("sendGroup"))[0]
        if group is not None:
            if message_type == 'image' or message_type == 'file':
                newFile = request.files.get('file')
                if newFile:
                    config2.mkdir(os.sep.join([config2.messageFilePath, message_type]))
                    save_path = os.sep.join([config2.messageFilePath, message_type, newFile.filename])
                    newFile.save(save_path)
                    message.content = save_path
                    try:
                        group.send_image(save_path)
                        return jsonify({'code': '000', 'msg': '发送成功', 'count': 0, 'data': ""})
                    except Exception as e:
                        return jsonify({'code': '001', 'msg': '发送失败', 'count': 0, 'data': e})
                else:
                    fileName = request.form.get("fileName")
                    fileContent = request.form.get("fileContent")
                    if fileName is None or fileName == "":
                        return jsonify({'code': '003', 'msg': '发送成功', 'count': 0, 'data': "文件名不能为空"})
                    if fileName is None or fileName == "":
                        return jsonify({'code': '003', 'msg': '发送成功', 'count': 0, 'data': "文件内容不能为空"})
                    message.content = base64util.bytes2file(fileName, fileContent)
                    db.session.add(message)
                    db.session.commit()
                    try:
                        group.send_image(message.content)
                        return jsonify({'code': '000', 'msg': '发送成功', 'count': 0, 'data': ""})
                    except Exception as e:
                        return jsonify({'code': '001', 'msg': '发送失败', 'count': 0, 'data': e})

            else:
                message.content = request.form.get("content")
                message.sendGroup = request.form.get("sendGroup")
                message.createTime = request.form.get("createTime")
                message.type = message_type
                db.session.add(message)
                db.session.commit()
                try:
                    group.send(message.content)
                    return jsonify({'code': '000', 'msg': '发送成功', 'count': 0, 'data': ""})
                except Exception as e:
                    return jsonify({'code': '001', 'msg': '发送失败', 'count': 0, 'data': e})

    except Exception as e:
        print(e)
        return jsonify({'code': '002', 'msg': '发送失败', 'count': 0, 'data': "没有那个群组"})
