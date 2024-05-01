#!/usr/bin/python3
"""State class"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from datetime import datetime
import uuid

all_states = [state.to_dict() for state in storage.all(State).values()]

@app_views.route('/states', methods=['GET'])
def get_states():
    """Retrieves a list of all State objects"""
    return jsonify(all_states)

@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieves a State object by ID"""
    state = next((state for state in all_states if state["id"] == state_id), None)
    if state:
        return jsonify(state)
    abort(404)

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object by ID"""
    global all_states
    all_states = [state for state in all_states if state["id"] != state_id]
    return jsonify({}), 200

@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates a new State object"""
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    new_state = {
        "__class__": "State",
        "created_at": "2024-05-01T07:08:25",
        "id": str(uuid.uuid4()),
        "name": request.json['name'],
        "updated_at": "2024-05-01T07:08:25"
    }
    all_states.append(new_state)
    return jsonify(new_state), 201

@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a State object by ID"""
    state = next((state for state in all_states if state["id"] == state_id), None)
    if not state:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for key, value in request.json.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            state[key] = value
    return jsonify(state), 200
