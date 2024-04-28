#!/usr/bin/python3
""" State Classes """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/states/', methods=['GET'])
def list_states():
    '''Retrieves a list of all State objects'''
    list_states = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(list_states)