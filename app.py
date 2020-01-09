import json
from operator import or_
from threading import Thread

from flask import Flask, request, jsonify, g
from wxpy import Bot, embed

import config
import model
import robot_config
from api_opt import api
from api_v1 import api_v1
from robot import robot
from ext import db, bot
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(config)
app.register_blueprint(api)
app.register_blueprint(api_v1)
db.init_app(app)
CORS(app, supports_credentials=True)
app.app_context().push()
print(app.app_context())

if __name__ == '__main__':
    app.run(host='192.168.10.130')
