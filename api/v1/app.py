from flask import Flask
"""
Using flask framework for building
"""

app = Flask(__name__)
"""Assigning app to Flask"""


@app.route("/")
def hello_world():
    """ Return Hello World """
    return "<p>Hello World!</p>"


if __name__ == "__main__":
    """ If script name is main """
    app.run(debug=True)
