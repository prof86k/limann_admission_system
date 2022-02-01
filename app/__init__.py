from config import DevConfig as admissionConf
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import flask_excel as excel


db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()
login_manager.login_view = 'auth.admin_login'
login_manager.session_protection = 'strong'
login_manager.login_message = 'Please login to access this page'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(userid):
    from .auth.models import Admin
    '''return the admin or the card info'''
    return Admin.query.get(int(userid))


def create_app():
    '''create app object from the function'''
    app = Flask(__name__)
    app.config.from_object(admissionConf)
    
    # late_init_app
    migrate.init_app(app=app, db=db, compare_type=True)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app=app)
    excel.init_excel(app)



    # return the blueprint instance
    from .auth import auth as auth_blueprint
    from .application import application as application_blueprint
    from .amin_site import admin_panel as admin_site_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(application_blueprint)
    app.register_blueprint(admin_site_blueprint)

    # return the app instance
    return app
