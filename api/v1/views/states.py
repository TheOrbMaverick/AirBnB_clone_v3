#!/usr/bin/python3
"""State class"""
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
    one_state_obj = [state.to_dict() for state in storage.all(State).values()
                     if state.id == state_id]
    if one_state_obj is None:
        abort(404)
    return jsonify(one_state_obj.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object"""
    one_state_obj = [state.to_dict() for state in storage.all(State).values()
                     if state.id == state_id]
    if one_state_obj is None:
        abort(404)
    storage.delete(one_state_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """Creates a State"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    one_state_obj = []
    new_state = State(name=request.json['name'])
    storage.new(new_state)
    storage.save()
    one_state_obj.append(new_state.to_dict())
    return jsonify(one_state_obj[0]), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    request_data = request.json
    if 'name' in request_data:
        state.name = request_data['name']
    storage.save()
    return jsonify(state.to_dict()), 200
