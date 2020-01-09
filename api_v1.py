import os

from flask import jsonify, request, Blueprint

import config2
from ext import db, bot
from model import SendMessage

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api_v1')


@api_v1.route("/addMessage", methods=['POST'])
def add_message():
    message_type = request.form.get("type")
    message = SendMessage()
    group = bot.groups().search(request.form.get("sendGroup"))[0]
    if message_type == 'image' or message_type == 'file':
        newFile = request.files.get('file')
        config2.mkdir(os.sep.join([config2.messageFilePath, newFile, message_type]))
        save_path = os.sep.join([config2.sourceSavePath, newFile.filename])
        newFile.save(save_path)
        message.content = save_path
        group.send_image(save_path)
    else:
        message.content = request.form.get("content")
        group.send(message.content)
    message.sendGroup = request.form.get("sendGroup")
    message.createTime = request.form.get("createTime")
    message.type = message_type
    db.session.add(message)
    db.session.commit()
    return jsonify({'code': '000', 'msg': '提交成功', 'count': 0, 'data': ""})
