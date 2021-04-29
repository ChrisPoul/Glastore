import os
from operator import attrgetter
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

    from .models.quote import Quote
    @app.context_processor
    def inject_sidebar_data():
        quotes = Quote.get_all()
        quotes = sorted(quotes, key=attrgetter('date'), reverse=True)
        return dict(
            sidebar_quotes=quotes
        )

    from .models import init_db_command
    app.cli.add_command(init_db_command)

    from .views import home
    app.register_blueprint(home.bp)

    from .views import auth
    app.register_blueprint(auth.bp)

    from .views import customer
    app.register_blueprint(customer.bp)

    from .views import product
    app.register_blueprint(product.bp)

    from .views import quote
    app.register_blueprint(quote.bp)

    return app
