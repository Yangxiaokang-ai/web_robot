import os

from wxpy import Bot

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = '1qaz!QAZ'
HOST = '192.168.10.179'
PORT = '3306'
DATABASE = 'robot'

SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
    DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
)
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
# BOT = Bot(cache_path=True, console_qr=True)
SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_MAX_OVERFLOW = 5

messageFilePath = os.sep.join(["/home", "deployer", "ReceiveFile", "message"])
replySavePath = os.sep.join(["/home", "deployer", "ReplyFile"])
g5_savePath = os.sep.join(["/home", "deployer", "g5_save"])
sourceSavePath = os.sep.join(["/home", "deployer", "ReceiveFile", "Answer"])
