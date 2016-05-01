
import os 

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")
track_modifications = app.config.setdefault(
    'SQLALCHEMY_TRACK_MODIFICATIONS',
    True,
)
db = SQLAlchemy(app)

from views import *
from errors import *


if __name__ == '__main__':
    app.run()