#!/usr/bin/python3
"""Amenity objects api"""

from flask import Flask, jsonify, abort, request
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


@app_views.route("/amenities", strict_slashes=False, methods=["GET"])
def all_amenities():
    amenities = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route("amenities/<amenity_id>", strict_slashes=False, methods=["GET"])
def get_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False, methods=["DELETE"])
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def add_amenity():
    if not request.get_json:
        abort(404, "Not a JSON")
    if "name" not in request.get_json:
        abort(404, "Missing name")
    amenities = []
    new_amenity = Amenity(name = request.json["name"])
    storage.new(new_amenity)
    storage.save()
    amenities.append(new_amenity.to_dict())
    return jsonify(amenities[0]), 201