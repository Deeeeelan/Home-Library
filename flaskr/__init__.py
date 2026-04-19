import os

from flask import Flask, render_template

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

	# init db
    from . import db
    db.init_app(app)
    
	# regiser auth
    from .api.auth import auth_bp
    app.register_blueprint(auth_bp)

    from .api.discovery import discovery_bp
    app.register_blueprint(discovery_bp)

    from .api.checkout import checkout_bp
    app.register_blueprint(checkout_bp)

    from .api.user import user_bp
    app.register_blueprint(user_bp)

    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/signup')
    def signup():
        return render_template('signup.html')


    return app