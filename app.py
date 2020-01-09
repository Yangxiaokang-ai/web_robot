import json
from operator import or_
from threading import Thread

from flask import Flask, request, jsonify, g
from sqlalchemy import desc
from wxpy import Bot, embed

import config
from model import ReplyLog
import robot_config
from api_opt import api
from api_v1 import api_v1
from ext import db, bot, scheduler
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(config)
app.register_blueprint(api)
app.register_blueprint(api_v1)
db.init_app(app)
CORS(app, supports_credentials=True)
app.app_context().push()

zb_sf = bot.groups().search("总部及省分OSS2.0")[0]


@scheduler.scheduler.scheduled_job(trigger='cron', id='send2Group', day_of_week='mon-fri', hour=10, minute=30)
def send2Group():
    with app.app_context():
        result = ReplyLog.query.filter(ReplyLog.msg_type == 'Text').order_by(desc(ReplyLog.message_createtime)).first()
        zb_sf.send(result.content)
        print(result.content)


@scheduler.scheduler.scheduled_job(trigger='cron', id='send2Group2', day_of_week='mon-fri', hour=10, minute=30)
def send2Group2():
    with app.app_context():
        result = ReplyLog.query.filter(ReplyLog.msg_type == 'Picture').order_by(
            desc(ReplyLog.message_createtime)).first()
        zb_sf.send_images(result.content)
        print(result.content)


print(app.app_context())
if __name__ == '__main__':
    scheduler.start()
    app.run(threaded=True)
