#!/usr/bin/python3
"""City class"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City


@app_views.route('/cities', strict_slashes=False, methods=['GET'])
def get_all_cities():
    """Retrieves the list of all City objects"""
    all_cities = [city.to_dict() for city in storage.all(City).values()]
    return jsonify(all_cities)


@app_views.route('/cities/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieves a City object"""
    city = storage.get(City, state_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<state_id>', strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """Deletes a City object"""
    city = storage.get(City, state_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities', strict_slashes=False, methods=['POST'])
def create_state():
    """Creates a City"""
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    new_state = City(**request.json)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/cities/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """Updates a City object"""
    city = storage.get(City, state_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    request_data = request.json
    request_data.pop('id', None)
    request_data.pop('created_at', None)
    request_data.pop('updated_at', None)
    for key, value in request_data.items():
        setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
