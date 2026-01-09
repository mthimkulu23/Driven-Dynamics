
import os

# Try to monkey-patch for eventlet as early as possible (before importing
# Flask/werkzeug) to avoid "Working outside of application/request context"
# errors when eventlet replaces networking internals.
use_eventlet = False
try:
    import eventlet
    eventlet.monkey_patch()
    use_eventlet = True
    print("Using eventlet monkey_patch (if installed)")
except Exception:
    # eventlet not installed or monkey_patch failed; we'll handle later
    use_eventlet = False

# Allow non-HTTPS OAuth callbacks in dev only
os.environ['AUTHLIB_INSECURE_TRANSPORT'] = 'true'

from app import create_app


app = create_app()


if __name__ == "__main__":
    # Import the package-level socketio instance
    from app import socketio

    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', '0') in ('1', 'true', 'True')

    if use_eventlet:
        print("Using eventlet for SocketIO (recommended for production)")
        socketio.run(app, debug=debug_mode, host="0.0.0.0", port=port)
    else:
        # Allow forcing Werkzeug in controlled deployments by setting
        # ALLOW_UNSAFE_WERKZEUG=1 (not recommended for production).
        allow_unsafe = os.environ.get('ALLOW_UNSAFE_WERKZEUG', '').lower() in ('1', 'true', 'yes')
        if allow_unsafe:
            print("WARNING: Running Werkzeug in production mode because ALLOW_UNSAFE_WERKZEUG is set.")
            socketio.run(app, debug=debug_mode, host="0.0.0.0", port=port, allow_unsafe_werkzeug=True)
        else:
            raise RuntimeError(
                "No asynchronous worker available (eventlet/gevent). "
                "Install 'eventlet' in requirements or set ALLOW_UNSAFE_WERKZEUG=1 to force Werkzeug (not recommended)."
            )