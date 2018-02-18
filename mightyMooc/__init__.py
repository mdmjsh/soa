from flask import Flask, current_app
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
with app.app_context():
	print(current_app.name)
	db = SQLAlchemy(app)
	migrate = Migrate(app, db)
	login = LoginManager(app)
	login.login_view = 'login'

	from mightyMooc import routes, models
