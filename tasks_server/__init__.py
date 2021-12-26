import os

from flask import Flask


def create_app(config_override=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, 'tasks.sqlite')
    )
    if config_override is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(config_override)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import inbox
    app.register_blueprint(inbox.inbox)

    return app


if __name__ == '__main__':
    create_app().run()
