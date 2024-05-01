#!/usr/bin/python3
""" Places api view"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_city_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a Place object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    if 'user_id' not in request.json:
        abort(400, "Missing user_id")
    if 'name' not in request.json:
        abort(400, "Missing name")
    user_id = request.json["user_id"]
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    place_data = request.json
    place_data['city_id'] = city_id
    place = Place(**place_data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.json
    # Ignore keys: id, user_id, city_id, created_at, updated_at
    data.pop('id', None)
    data.pop('user_id', None)
    data.pop('city_id', None)
    data.pop('created_at', None)
    data.pop('updated_at', None)
    for key, value in data.items():
        setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'])
def places_search():
    # Check if request contains JSON data
    if not request.is_json:
        abort(400, 'Not a JSON')

    # Retrieve JSON data from request
    data = request.get_json()

    # Extract states, cities, and amenities from JSON data
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    # Initialize list to store matching places
    matching_places = []

    # Retrieve all places if no states, cities, or amenities specified
    if not (states or cities or amenities):
        matching_places = storage.all(Place).values()
    else:
        # Retrieve places based on states
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                matching_places.extend(state.places)

        # Retrieve places based on cities
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                matching_places.extend(city.places)

        # Filter places based on amenities
        for amenity_id in amenities:
            matching_places = [place for place in matching_places if amenity_id in place.amenities]

    # Convert matching places to dictionary format
    places_dict = [place.to_dict() for place in matching_places]

    return jsonify(places_dict)
