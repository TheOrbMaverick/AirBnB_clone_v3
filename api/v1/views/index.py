#!/usr/bin/python3
""" Doing the index for flask """

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


classes = {"users": User, "places": Place, "states": State,
           "cities": City, "amenities": Amenity,
           "reviews": Review}


@app_views.route("/status", strict_slashes=False, methods=["GET"])
def status():
    """ Status page """
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False, methods=["GET"])
def stats():
    """ Return the full count """
    number_of = {}
    for cls in classes:
        number_of[cls] = int(storage.count(classes[cls]))
    return jsonify(number_of)
