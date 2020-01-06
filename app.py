from flask import Flask

import config
import model
import robot_config
from ext import db

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
app.app_context().push()
print(robot_config.get_text_from_robot("你好"))
print(robot_config.getAddress("王磊"))


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


if __name__ == '__main__':
    app.run()
