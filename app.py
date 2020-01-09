from flask import Flask
from flask_cors import CORS

import config
from api_opt import api
from api_v1 import api_v1
from ext import db, scheduler

app = Flask(__name__)
app.config.from_object(config)
app.register_blueprint(api)
app.register_blueprint(api_v1)
db.init_app(app)
CORS(app, supports_credentials=True)

scheduler.init_app(app)
scheduler.start()


@scheduler.scheduler.scheduled_job(trigger='interval', id='apscheduler', seconds=1)
def apscheduler():
    print("APScheduler start")


app.app_context().push()
print(app.app_context())

if __name__ == '__main__':
    app.run(host='192.168.10.130')
