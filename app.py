from flask import Flask
from flask_cors import CORS

import config
from api_opt import api
from api_v1 import api_v1
from ext import db, bot, scheduler

app = Flask(__name__)
app.config.from_object(config)
app.register_blueprint(api)
app.register_blueprint(api_v1)
db.init_app(app)
CORS(app, supports_credentials=True)
app.app_context().push()
bot.file_helper.send('Hello from wxpy!')
test = bot.groups().search("总部及省分OSS2.0")[0]


@scheduler.scheduler.scheduled_job(trigger='interval', id='myheart', hours=1)
def myheart():
    bot.file_helper.send('Hello from wxpy!')


'''
@scheduler.scheduler.scheduled_job(trigger='cron', id='send2Group', day_of_week='0-6', hour=10, minute=30)
def send2Group():
    with app.app_context():
        if is_workday(datetime.date.today()):
            result = model.ReplyLog.query.filter(model.ReplyLog.msg_type == 'Text').order_by(desc(
                model.ReplyLog.message_createtime)).first()
            test.send(result.content)
            print(result.content)

'''

'''
@scheduler.scheduler.scheduled_job(trigger='cron', id='send2Group2', day_of_week='0-6', hour=10, minute=30)
def send2Group2():
    with app.app_context():
        if is_workday(datetime.date.today()):
            result = model.ReplyLog.query.filter(model.ReplyLog.msg_type == 'Picture').order_by(desc(
                model.ReplyLog.message_createtime)).first()
            test.send_image(result.content)
            print(result.content)

'''
print(app.app_context())
if __name__ == '__main__':
    # scheduler.start()
    app.run()
   # app.run(host='10.126.141.229', port=8999, threaded=True)
