#!/usr/bin/python3
"""City objects api"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False, methods=['GET'])
def get_state_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(City, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', strict_slashes=False, methods=['POST'])
def create_city(state_id):
    """Creates a City"""
    state = storage.get(City, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    data = request.json
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.json
    data.pop('id', None)
    data.pop('state_id', None)
    data.pop('created_at', None)
    data.pop('updated_at', None)
    for key, value in data.items():
        setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
