#!/usr/bin/python3
"""
Using flask framework for building
"""
import sys
sys.path.append('/Users/macbookair/Documents/ALX/AirBnB_clone_v3')
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.route("/")
def hello_world():
    """ Return Hello World """
    return "<p>Hello World!</p>"

@app.teardown_appcontext
def teardown(self):
    """Close the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    """ If script name is main """
    if getenv("HBNB_API_HOST") is None:
        HBNB_API_HOST = '0.0.0.0'
    else:
        HBNB_API_HOST = getenv("HBNB_API_HOST")
    if getenv("HBNB_API_PORT") is None:
        HBNB_API_PORT = 5000
    else:
        HBNB_API_PORT = int(getenv("HBNB_API_PORT"))
    app.run(debug=True, host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
