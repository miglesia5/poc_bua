from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from bua.config import Config

from flask_admin import Admin

from flask_admin.contrib.sqla import ModelView



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'squads.login'
login_manager.login_message_category = 'info'
mail = Mail()





def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    admin = Admin(app)

    from bua.views_and_forms.squads.routes import squads
    from bua.views_and_forms.tasks.routes import tasks
    from bua.views_and_forms.main.routes import main
    from bua.views_and_forms.errors.handlers import errors
    from bua.views_and_forms.action.to_do import todo

    app.register_blueprint(squads)
    app.register_blueprint(tasks)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(todo)





    return app

