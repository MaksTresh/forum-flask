from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
login = LoginManager(app)

from app import routes, models