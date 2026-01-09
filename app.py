
import os

# Allow non-HTTPS OAuth callbacks in dev only
os.environ['AUTHLIB_INSECURE_TRANSPORT'] = 'true'

from app import create_app


app = create_app()


if __name__ == "__main__":
    # Import the package-level socketio instance
    from app import socketio

    # Prefer a production-ready async worker (eventlet). If not available,
    # fall back to socketio.run with allow_unsafe_werkzeug only when explicitly
    # permitted by the environment.
    use_eventlet = False
    try:
        import eventlet
        # monkey patch for eventlet
        eventlet.monkey_patch()
        use_eventlet = True
        print("Using eventlet for SocketIO (recommended for production)")
    except Exception:
        print("eventlet not available — falling back to socketio.run")

    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', '0') in ('1', 'true', 'True')

    if use_eventlet:
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