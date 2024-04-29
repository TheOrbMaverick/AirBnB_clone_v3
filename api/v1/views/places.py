#!/usr/bin/python3
"""places"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from datetime import datetime
import uuid


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def list_places(city_id):
    """ Retrieves a list of all Place objects """

    list_stored_places = [obj.to_dict() for obj in storage.all("City").values()
                          if obj.id == city_id]
    if list_stored_places == []:
        abort(404)
    return jsonify(list_stored_places)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_place(place_id):
    '''Retrieves an Place object'''
    all_stored_places = storage.all("Place").values()
    one_place_obj = [
        obj.to_dict() for obj in all_stored_places if obj.id == place_id
        ]
    if one_place_obj == []:
        abort(404)
    return jsonify(one_place_obj[0])


@app_views.route(
        '/places/<place_id>', strict_slashes=False, methods=['DELETE']
        )
def delete_place(place_id):
    '''Deletes an Place object'''
    all_stored_places = storage.all("Place").values()
    one_place_obj = [
        obj.to_dict() for obj in all_stored_places if obj.id == place_id
        ]
    if one_place_obj == []:
        abort(404)
    one_place_obj.remove(one_place_obj[0])
    for obj in all_stored_places:
        if obj.id == place_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/places/', strict_slashes=False, methods=['POST'])
def create_place():
    '''Creates an Place'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    places = []
    new_place = Place(name=request.json['name'])
    storage.new(new_place)
    storage.save()
    places.append(new_place.to_dict())
    return jsonify(places[0]), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def updates_place(place_id):
    '''Updates an Place object'''
    all_stored_places = storage.all("Place").values()
    one_place_obj = [
        obj.to_dict() for obj in all_stored_places if obj.id == place_id
        ]
    if one_place_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    one_place_obj[0]['name'] = request.json['name']
    for obj in all_stored_places:
        if obj.id == place_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(one_place_obj[0]), 200
