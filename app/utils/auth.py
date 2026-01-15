from functools import wraps
from flask import session, redirect, url_for, flash, render_template


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
                # Render a clear permission denied page (HTTP 403) instead of silently
                # sending sellers back to the landing page. This makes it explicit
                # that the resource is restricted to a different role.
                try:
                    return render_template('permission_denied.html'), 403
                except Exception:
                    # Fallback: if the template is missing, redirect to login
                    return redirect(url_for('users.login'))
            return f(*args, **kwargs)
        return decorated
    return decorator


def role_required_any(*roles):
    """Decorator factory to allow any of the provided roles.

    Usage: @role_required_any('seller', 'admin')
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user_role = session.get('user_role')
            if not user_role:
                flash('Please log in to access this page.', 'error')
                return redirect(url_for('users.login'))
            if user_role not in roles:
                flash('You do not have permission to access this resource.', 'error')
                try:
                    return render_template('permission_denied.html'), 403
                except Exception:
                    return redirect(url_for('users.login'))
            return f(*args, **kwargs)
        return decorated
    return decorator
