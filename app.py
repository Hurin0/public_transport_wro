from flask_migrate import Migrate

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from . import config


app = Flask(__name__)
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_SIZE'] = 20
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 20
app.config['SQLALCHEMY_POOL_RECYCLE'] = 1800
app.app_context().push()
db = SQLAlchemy(app)

migrate = Migrate(app, db, compare_type=True)




