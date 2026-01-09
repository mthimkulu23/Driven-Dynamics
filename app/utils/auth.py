from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    """Decorator to require a logged-in user (checks session['user_email'])."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_email' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('users.login'))
        return f(*args, **kwargs)
    return decorated


def role_required(role):
    """Decorator factory to require a specific user role stored in session['user_role']."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user_role = session.get('user_role')
            if not user_role:
                flash('Please log in to access this page.', 'error')
                return redirect(url_for('users.login'))
            if user_role != role:
                flash('You do not have permission to access this resource.', 'error')
                # Redirect to a sensible landing based on role
                if user_role == 'seller':
                    return redirect(url_for('users.landing'))
                else:
                    return redirect(url_for('users.login'))
            return f(*args, **kwargs)
        return decorated
    return decorator
