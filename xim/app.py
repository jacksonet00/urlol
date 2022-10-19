from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from secret import db_uri, secret_key
from os import environ
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.update({
    'SQLALCHEMY_DATABASE_URI': db_uri,
    'SECRET_KEY': secret_key
})

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


if __name__ == "__main__":
    from views import *

    app.run(host='0.0.0.0', debug=True, port=environ.get('PORT'))
