from flask import Blueprint

from .models import Admin, Role
from .. import db

auth = Blueprint('auth', __name__, url_prefix='/')

from . import views, errors, forms


@auth.before_request
def create_admin():
    if not Admin.query.filter(Admin.username == 'admin086').first():
        a = Admin(username='admin086', email='kkumasampson@gmail.com')
        a.set_password_to_hash('086byadmin')
        a.roles.append(Role(name='admin'))
        a.roles.append(Role(name='card_seller'))
        db.session.add(a)
        db.session.commit()
    elif not Admin.query.filter(Admin.username == 'admin086').first().has_role('card_seller'):
        a = Admin.query.filter(Admin.username == 'admin086').first()
        a.roles.append(Role(name='card_seller'))
        db.session.commit()


    
