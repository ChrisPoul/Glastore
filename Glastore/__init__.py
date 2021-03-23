import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{app.instance_path}/Glastore.sqlite"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "dev"

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .models import db
    db.init_app(app)

    from .models import init_db_command
    app.cli.add_command(init_db_command)

    from . import home
    app.register_blueprint(home.bp)

    from . import customer
    app.register_blueprint(customer.bp)

    from . import product
    app.register_blueprint(product.bp)

    from . import quote
    app.register_blueprint(quote.bp)

    return app
