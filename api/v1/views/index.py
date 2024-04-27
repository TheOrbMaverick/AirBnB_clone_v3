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

classes = {"users": "User", "places": "Place", "states": "State",
           "cities": "City", "amenities": "Amenity",
           "reviews": "Review"}


@app_views.route("/status", methods=["GET"])
def status():
    """ Status page """
    return jsonify({"status": "OK"})

@app_views.route("/stats", methods=["GET"])
def count():
    """ Get total number of instances"""
    count_d = {}
    for cls in classes:
        count_d[cls] = storage.count(classes[cls])
    return jsonify(count_d)
