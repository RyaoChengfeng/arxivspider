from flask import Flask
import os
from flask_script import Shell


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.update(test_config)

    from . import db
    db.init_app(app)

    from . import bp
    app.register_blueprint(bp)

    return app


