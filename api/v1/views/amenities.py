#!/usr/bin/python3
""" Amenity api views """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'])
def list_amenities():
    """ Retrieves a list of all Amenity objects """
    all_amenities = [obj.to_dict() for obj in storage.all("Amenity").values()]
    return jsonify(all_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """ Retrieve one Amenity object """
    amenities = storage.all("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in amenities
                   if obj.id == amenity_id]
    if amenity_obj == []:
        abort(404)
    return jsonify(amenity_obj[0])


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ Deletes one Amenity object """
    amenities = storage.all("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in amenities
                   if obj.id == amenity_id]
    if amenity_obj == []:
        abort(404)
    amenity_obj.remove(amenity_obj[0])
    for obj in amenities:
        if obj.id == amenity_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    """ Create one Amenity """
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    amenities_list = []
    new_amenity = Amenity(name=request.json['name'])
    storage.new(new_amenity)
    storage.save()
    amenities_list.append(new_amenity.to_dict())
    return jsonify(amenities_list[0]), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def updates_amenity(amenity_id):
    """ Updates an Amenity object """
    amenities = storage.all("Amenity").values()
    amenity_obj = [obj.dict() for obj in amenities
                   if obj.id == amenity_id]
    if amenity_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    amenity_obj[0]["name"] = request.json["name"]
    for obj in amenities:
        if obj.id == amenity_id:
            obj.name = request.json["name"]
    storage.save()
    return jsonify(amenity_obj[0]), 200
