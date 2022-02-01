from functools import wraps
from flask_login import current_user
from flask import abort


def has_role(name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args,**kwargs):
            if current_user.has_role(name):
                return f(*args,**kwargs)
            else:
                abort(403)
        return wrapper
    return decorator