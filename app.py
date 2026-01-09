
import os
os.environ['AUTHLIB_INSECURE_TRANSPORT'] = 'true'
from app import create_app


app = create_app()



if __name__ == "__main__":
    # Use SocketIO's runner so websocket/socket connections work.
    # Import socketio from the app package (it's created at package-level).
    from app import socketio

    socketio.run(app, debug=True, host="0.0.0.0", port=5000)