from flask import Flask
from flask_login import LoginManager
from application.config import Config
from application.database import db

app=None
DB_NAME = "project.sqlite3"

def create_app():
    app = Flask(__name__,template_folder='templates')
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = '480627f8209a377319dfe2fdbbfeb145234907922af3dc2b96365d6c9bf4420b'
    db.init_app(app)
    app.app_context().push()
    return  app

app= create_app()
from application.controllers import *


from application.models import Users
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=False)