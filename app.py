from secret import DB_URI, SECRET_KEY

from os import environ

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.update({
    'SQLALCHEMY_DATABASE_URI': DB_URI,
    'SECRET_KEY': SECRET_KEY
})

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


if __name__ == "__main__":
    from views import *
    from loader import *

    app.run(host='0.0.0.0', debug=True, port=environ.get('PORT'))
