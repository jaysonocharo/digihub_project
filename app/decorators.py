from functools import wraps
from flask import abort
from flask_login import current_user

def role_required(role):
    """Restrict access to users with a specific role."""
    def decorator(f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                abort(403)  
            return f(*args, **kwargs)
        return wrapped_function
    return decorator
