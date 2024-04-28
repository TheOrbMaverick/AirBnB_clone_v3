#!/usr/bin/python3
""" State Classes """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/states/', methods=['GET'])
def list_all_states():
    '''Retrieves a list of all State objects'''
    list_states = []
    for obj in storage.all("State").keys():
        obj_dict = obj.to_dict()
        list_states.append(obj_dict)
    return jsonify(list_states)


@app_views.route('/states/<states_id>', methods=['GET'])
def list_state_by_id(state_id):
    list_states = []
    state_id
    for obj in storage.all("State").values():
        if obj.id == state_id:
            obj_dict = obj.to_dict()
            list_states.append(obj_dict)
        else:
            abort(404)
