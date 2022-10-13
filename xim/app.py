from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from secret import db_uri
from os import environ

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)


if __name__ == "__main__":
    from views import *

    app.run(host='0.0.0.0', debug=True, port=environ.get('PORT'))
