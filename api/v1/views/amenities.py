#!/usr/bin/python3
"""amenities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from datetime import datetime
import uuid


@app_views.route('/amenities/', strict_slashes=False, methods=['GET'])
def list_amenities():
    '''Retrieves a list of all Amenity objects'''
    list_stored_amenities = [obj.to_dict() for obj in storage.all("Amenity").values()]
    return jsonify(list_stored_amenities)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['GET'])
def get_amenity(amenity_id):
    '''Retrieves an Amenity object'''
    all_stored_amenities = storage.all("Amenity").values()
    one_amenity_obj = [obj.to_dict() for obj in all_stored_amenities
                   if obj.id == amenity_id]
    if one_amenity_obj == []:
        abort(404)
    return jsonify(one_amenity_obj[0])


@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['DELETE'])
def delete_amenity(amenity_id):
    '''Deletes an Amenity object'''
    all_stored_amenities = storage.all("Amenity").values()
    one_amenity_obj = [obj.to_dict() for obj in all_stored_amenities
                   if obj.id == amenity_id]
    if one_amenity_obj == []:
        abort(404)
    one_amenity_obj.remove(one_amenity_obj[0])
    for obj in all_stored_amenities:
        if obj.id == amenity_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', strict_slashes=False, methods=['POST'])
def create_amenity():
    '''Creates an Amenity'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    amenities = []
    new_amenity = Amenity(name=request.json['name'])
    storage.new(new_amenity)
    storage.save()
    amenities.append(new_amenity.to_dict())
    return jsonify(amenities[0]), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['PUT'])
def updates_amenity(amenity_id):
    '''Updates an Amenity object'''
    all_stored_amenities = storage.all("Amenity").values()
    one_amenity_obj = [obj.to_dict() for obj in all_stored_amenities
                   if obj.id == amenity_id]
    if one_amenity_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    one_amenity_obj[0]['name'] = request.json['name']
    for obj in all_stored_amenities:
        if obj.id == amenity_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(one_amenity_obj[0]), 200
