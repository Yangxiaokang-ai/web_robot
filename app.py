import json
from operator import or_

from flask import Flask, request, jsonify

import config
import model
import robot_config
from api_opt import api
from ext import db
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(config)
app.register_blueprint(api)
db.init_app(app)
CORS(app, supports_credentials=True)
app.app_context().push()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/addTest")
def add_test():
    test = model.Config()
    test.name = "test"
    test.value = "1111"
    test.createtime = "111"
    db.session.add(test)
    db.session.commit()
    return "111"


@app.route("/queryUser", methods=['POST'])
def queryUser():
    page = request.args.get('page', 1, type=int)
    rows = request.args.get('rows', 10, type=int)
    count = model.User.query.count()
    users = model.User.query.filter().offset(rows * (page - 1)).limit(10).all()
    print(users)
    print(json.dumps(users))
    for user in users:
        print(user.trueName)
    return jsonify({'code': '000', 'msg': '查询成功', 'count': count})


if __name__ == '__main__':
    app.run(host='192.168.10.130')
