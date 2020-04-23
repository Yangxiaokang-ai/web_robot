from flask_sqlalchemy import SQLAlchemy
from wxpy import Bot
from flask_apscheduler import APScheduler

scheduler = APScheduler()
db = SQLAlchemy()
# bot = Bot(cache_path=True, console_qr=True)
