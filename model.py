from ext import db


class Config(db.Model):
    __tablename__ = 't_config'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    value = db.Column(db.String(255))
    createtime = db.Column(db.String(255))


class User(db.Model):
    __tablename__ = 'user2'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orgNum = db.Column(db.String(255))
    userId = db.Column(db.String(255))
    orgId = db.Column(db.String(255))
    userName = db.Column(db.String(255))
    trueName = db.Column(db.String(255))
    mobliePhone = db.Column(db.String(255))
    telPhone = db.Column(db.String(255))
    email = db.Column(db.String(255))
    deptName2 = db.Column(db.String(255))
    pid = db.Column(db.String(255))
    deptName = db.Column(db.String(255))

    def jsonStr(self):
        jsonData = {
            'id': self.id,
            'userName': self.userName,

        }
        return jsonData


class MessageLog(db.Model):
    __tablename__ = 'message_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    message_sender = db.Column(db.String(255))
    message_type = db.Column(db.String(255))
    message_createtime = db.Column(db.String(255))


class MessageLogZwzx(db.Model):
    __tablename__ = 'message_log_dept_zwzx'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    message_sender = db.Column(db.String(255))
    message_type = db.Column(db.String(255))
    message_createtime = db.Column(db.String(255))


class Questions(db.Model):
    __tablename__ = 't_question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String(255))
    answer = db.Column(db.Text)
    answer_type = db.Column(db.String(255))
    keywords = db.Column(db.String(255))


class ReplyLog(db.Model):
    __tablename__ = 'reply_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    message_createtime = db.Column(db.String(255))
    msg_type = db.Column(db.String(255))


class BotConfig(db.Model):
    __tablename__ = 'bot_config'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    createtime = db.Column(db.String(255))
    type = db.Column(db.String(255))
    log_table = db.Column(db.String(255))
