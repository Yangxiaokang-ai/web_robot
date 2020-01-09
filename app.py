from flask import Flask
from flask_cors import CORS
from sqlalchemy import desc

import config
from api_opt import api
from api_v1 import api_v1
from ext import db, scheduler, bot
from model import ReplyLog

app = Flask(__name__)
app.config.from_object(config)
app.register_blueprint(api)
app.register_blueprint(api_v1)
db.init_app(app)
CORS(app, supports_credentials=True)
test2 = bot.groups().search("测试2")
scheduler.init_app(app)
scheduler.start()

app.app_context().push()


@scheduler.scheduler.scheduled_job(trigger='interval', id='send2Group', seconds=2)
def send2Group():
    with app.app_context():
        result = ReplyLog.query.filter(ReplyLog.msg_type == 'Text').order_by(desc(ReplyLog.message_createtime)).first()
        test2[0].send(result.content)


@scheduler.scheduler.scheduled_job(trigger='interval', id='send2Group', seconds=2)
def send2Group():
    with app.app_context():
        result = ReplyLog.query.filter(ReplyLog.msg_type == 'Text').order_by(desc(ReplyLog.message_createtime)).first()
        test2[0].send_images(result.content)


if __name__ == '__main__':
    app.run(host='192.168.10.130')
