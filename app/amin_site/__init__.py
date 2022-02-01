from flask import Blueprint


admin_panel = Blueprint('admin_panel',__name__,url_prefix='/admin')

from . import views, errors,logics,settings