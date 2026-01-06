
import os
os.environ['AUTHLIB_INSECURE_TRANSPORT'] = 'true'
from app import create_app


app = create_app()



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(5000))