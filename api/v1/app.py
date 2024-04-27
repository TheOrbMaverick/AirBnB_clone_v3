from flask import Flask, jsonify
import models
from api.v1.views import app_views
import os
"""
Using flask framework for building
"""

app = Flask(__name__)
"""Assigning app to Flask"""

# Register the blueprint app_views to your Flask instance app
app.register_blueprint(app_views)


@app.route("/")
def hello_world():
    """ Return Hello World """
    return "<p>Hello World!</p>"


# Declare a method to handle teardown_appcontext that calls storage.close()
@app.teardown_appcontext
def teardown_appcontext(exception):
    """Close the current SQLAlchemy session."""
    models.storage.close()


if __name__ == "__main__":
    """ If script name is main """
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(debug=True, host=host, port=port, threaded=True)
