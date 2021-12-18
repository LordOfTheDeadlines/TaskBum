from flask import Flask

from config.config import Configuration
from modules.database import db
from flask_login import LoginManager
from views import taskbum
from auth import auth

app = Flask(__name__, static_folder="static")
app.config.from_object(Configuration)

app.register_blueprint(taskbum, url_prefix='/taskbum')
app.register_blueprint(auth, url_prefix='/auth')

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

db.init_app(app)
db.app = app
db.create_all()

from models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
