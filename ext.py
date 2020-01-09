from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from wxpy import Bot

db = SQLAlchemy()
scheduler = APScheduler()
# bot = Bot(cache_path=True, console_qr=True)

bot = None
