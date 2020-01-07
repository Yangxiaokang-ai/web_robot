import json
import os

from flask import jsonify, request, Blueprint
from sqlalchemy import or_, and_
from werkzeug.utils import secure_filename

import robot_config
from ext import db
from model import User, BotConfig, Questions

api = Blueprint('api', __name__, url_prefix='/api')


class JSONHelper():
    @staticmethod
    def jsonBList(beans):
        result = []
        for item in beans:
            result.append(serialize(item))
        return result


def serialize(model):
    from sqlalchemy.orm import class_mapper
    columns = [c.key for c in class_mapper(model.__class__).columns]
    return dict((c, getattr(model, c)) for c in columns)


@api.route("/queryUser", methods=['POST'])
def queryUser():
    page = request.form.get('page', 1, type=int)
    rows = request.form.get('rows', 10, type=int)
    params = request.form.get('params', '')
    if params == '':
        count = User.query.count()
        users = User.query.filter().offset(rows * (page - 1)).limit(rows).all()
    else:
        count = User.query.filter(or_(User.trueName.like("%" + params + "%"), User.deptName2.like("%" + params + "%"),
                                      User.deptName.like("%" + params + "%"))).count()
        users = User.query.filter(or_(User.trueName.like("%" + params + "%"), User.deptName2.like("%" + params + "%"),
                                      User.deptName.like("%" + params + "%"))).offset(rows * (page - 1)).limit(
            rows).all()
    return jsonify({'code': '000', 'msg': '查询成功', 'count': count, 'data': JSONHelper.jsonBList(users)})


@api.route("/queryBotConfig", methods=['POST'])
def queryBotConfig():
    page = request.form.get('page', 1, type=int)
    rows = request.form.get('rows', 10, type=int)
    params = request.form.get('params', '')

    if params == '':
        count = BotConfig.query.count()
        botConfig = BotConfig.query.filter().offset(rows * (page - 1)).limit(10).all()
    else:
        count = BotConfig.query.filter(or_(BotConfig.type == params, BotConfig.name.like("%" + params + "%"))).count()
        botConfig = BotConfig.query.filter(
            or_(BotConfig.type == params, BotConfig.name.like("%" + params + "%"))).offset(rows * (page - 1)).limit(
            rows).all()
    return jsonify({'code': '000', 'msg': '查询成功', 'count': count, 'data': JSONHelper.jsonBList(botConfig)})


@api.route("/addBotConfig", methods=['put'])
def addBotConfig():
    botConfig = BotConfig()
    botConfig.name = request.form.get('name')
    botConfig.type = request.form.get('type')
    botConfig.createtime = request.form.get("createTime")
    db.session.add(botConfig)
    db.session.commit()
    return jsonify({'code': '000', 'msg': '提交成功', 'count': 0, 'data': ""})


@api.route("/delBotConfig", methods=['DELETE'])
def delBotConfig():
    ids = request.form.get("ids")
    print(ids)
    try:
        BotConfig.query.filter(BotConfig.id.in_(ids.split(","))).delete(synchronize_session=False)
        db.session.commit()
        return jsonify({'code': '000', 'msg': '删除成功', 'count': 0, 'data': ""})
    except Exception as e:
        print(e)
        return jsonify({'code': '001', 'msg': '删除失败', 'count': 0, 'data': ""})


@api.route("updateBotConfig", methods=['POST'])
def updateBotConfig():
    BotConfig.query.filter(BotConfig.id == request.form.get("id")).update(json.loads(request.form.get('data')),
                                                                          synchronize_session=False)
    return jsonify({'code': '000', 'msg': '修改成功', 'count': 0, 'data': ""})


@api.route("queryQuestions", methods=['POST'])
def queryQuestion():
    page = request.form.get('page', 1, type=int)
    rows = request.form.get('rows', 10, type=int)
    params = request.form.get('params', '')
    questionType = request.form.get('type', '')
    condition = (1 == 1)
    if questionType != '':
        condition = and_(Questions.answer_type == questionType)
    if params != '':
        condition = and_(condition,
                         or_(Questions.answer.like("%" + params + "%"), Questions.question.like("%" + params + "%"),
                             Questions.keywords.like("%" + params + "%")))
    a = Questions.query.filter(condition)
    count = a.count()
    data = a.limit(rows).offset(rows * (page - 1)).all()
    return jsonify({'code': '000', 'msg': '查询成功', 'count': count, 'data': JSONHelper.jsonBList(data)})


@api.route("addQuestions", methods=['PUT'])
def addQuestion():
    question = Questions()
    answer_type = request.form.get('answer_type')

    if answer_type == 'File' or answer_type == 'Images':
        newFile = request.files.get('file')
        save_path = os.sep.join([robot_config.sourceSavePath, newFile.filename])
        newFile.save(save_path)
        question.answer = save_path

    else:
        question.answer = request.form.get("answer")
    question.question = request.form.get("question")
    question.answer_type = request.form.get("answer_type")
    question.keywords = request.form.get("keywords")
    db.session.add(question)
    db.session.commit()
    return jsonify({'code': '000', 'msg': '提交成功', 'count': 0, 'data': ""})


@api.route("/updateQuestions", methods=['POST'])
def updateQuestion():
    answer_type = request.form.get('answer_type')
    jsons = json.loads(request.form.get('data'))
    print(jsons)
    if answer_type == 'File' or answer_type == 'Images':
        newFile = request.files.get('file')
        save_path = os.sep.join([robot_config.sourceSavePath, newFile.filename])
        newFile.save(save_path)
        jsons['answer'] = save_path
    Questions.query.filter(Questions.id == request.form.get("id")).update(jsons, synchronize_session=False)
    db.session.commit()
    return jsonify({'code': '000', 'msg': '提交成功', 'count': 0, 'data': ""})


@api.route("/delQuestions", methods=['DELETE'])
def delQuestions():
    ids = request.form.get("ids")
    print(ids)
    try:
        Questions.query.filter(Questions.id.in_(ids.split(","))).delete(synchronize_session=False)
        db.session.commit()
        return jsonify({'code': '000', 'msg': '删除成功', 'count': 0, 'data': ""})
    except Exception as e:
        print(e)
        return jsonify({'code': '001', 'msg': '删除失败', 'count': 0, 'data': ""})
