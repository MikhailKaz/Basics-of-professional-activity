# Flask modules
from flask import Flask


def create_app(debug: bool = False) -> Flask:
    # Initialize app
    app = Flask(__name__, template_folder='../templates')

    # Setup app configs
    app.config['DEBUG'] = debug
    app.config['SECRET_KEY'] = 'my secret'

    # Initialize extensions
    from app.extensions import bcrypt, csrf, login_manager
    csrf.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from app.routes import routes
    app.register_blueprint(routes)

    return app
