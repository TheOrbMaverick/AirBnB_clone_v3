#!/usr/bin/python3
"""State class"""
import sys
sys.path.append("/Users/macbookair/Documents/ALX/AirBnB_clone_v3")
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from datetime import datetime


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_all_states():
    """Retrieves the list of all State objects"""
    all_states = [state.to_dict() for state in storage.all(State).values()]
    print(all_states)
    return jsonify(all_states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """Creates a State"""
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    new_state = State(**request.json)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """Updates a State object"""
    all_states = storage.all("State").values()
    one_state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if one_state_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    one_state_obj[0]["name"] = request.json["name"]
    for obj in all_states:
        if obj.id == state_id:
            obj.name = request.json["name"]
    storage.save()
    return jsonify(one_state_obj[0]), 200
