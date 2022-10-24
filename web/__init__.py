from .secret import SECRET_KEY, DB_URI
from .model.core import db

import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        SQLALCHEMY_DATABASE_URI=DB_URI,
    )

    if not test_config:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    from .view import auth
    app.register_blueprint(auth.bp)

    from .view import dashboard
    app.register_blueprint(dashboard.bp)
    app.add_url_rule('/', endpoint='index')

    from .view import alias
    app.register_blueprint(alias.bp)

    from .view import search
    app.register_blueprint(search.bp)

    return app
