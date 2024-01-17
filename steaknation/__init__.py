from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '01512b8c8baffccbbb5e4e1466ebdc5d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservations.db'

db = SQLAlchemy(app)
flask_bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "warning"

ADMIN_NAME = 'ADMIN'
ADMIN_PHONE_NUMBER = "0000000000"

from steaknation import routes
