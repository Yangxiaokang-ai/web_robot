from flask_sqlalchemy import SQLAlchemy
from wxpy import Bot

db = SQLAlchemy()
bot = Bot(cache_path=True, console_qr=True)
