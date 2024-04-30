#!/usr/bin/python3
""" Using flask framework for building """
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.route("/")
def hello_world():
    """ Return Hello World """
    return "<p>Hello World!</p>"


@app.teardown_appcontext
def tear(self):
    """Close the current SQLAlchemy session."""
    storage.close()


@app.errorhandler(404)
def unfounded(error):
    """ Handle 404 unfound page """
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    """ If script name is main """
    if getenv("HBNB_API_HOST") is None:
        HBNB_API_HOST = '0.0.0.0'
    else:
        HBNB_API_HOST = getenv("HBNB_API_HOST")
    if getenv("HBNB_API_PORT") is None:
        HBNB_API_PORT = 3000
    else:
        HBNB_API_PORT = int(getenv("HBNB_API_PORT"))
    app.run(debug=True, host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
