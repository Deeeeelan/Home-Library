from datetime import datetime
from flask import current_app, g

def close_db():
    pass

def init_db_command():
    pass

def init_app(app):
    print('init')
    # app.teardown_appcontext(close_db)
    # app.cli.add_command(init_db_command)