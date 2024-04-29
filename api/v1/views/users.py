#!/usr/bin/python3
"""users"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from datetime import datetime
import uuid


@app_views.route('/users/', strict_slashes=False, methods=['GET'])
def list_users():
    '''Retrieves a list of all User objects'''
    list_stored_users = [obj.to_dict() for obj in storage.all("User").values()]
    return jsonify(list_stored_users)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user(user_id):
    '''Retrieves an User object'''
    all_stored_users = storage.all("User").values()
    one_user_obj = [obj.to_dict() for obj in all_stored_users
                   if obj.id == user_id]
    if one_user_obj == []:
        abort(404)
    return jsonify(one_user_obj[0])


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    '''Deletes an User object'''
    all_stored_users = storage.all("User").values()
    one_user_obj = [obj.to_dict() for obj in all_stored_users
                   if obj.id == user_id]
    if one_user_obj == []:
        abort(404)
    one_user_obj.remove(one_user_obj[0])
    for obj in all_stored_users:
        if obj.id == user_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/users/', strict_slashes=False, methods=['POST'])
def create_user():
    '''Creates an User'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    users = []
    new_user = User(name=request.json['name'])
    storage.new(new_user)
    storage.save()
    users.append(new_user.to_dict())
    return jsonify(users[0]), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def updates_user(user_id):
    '''Updates an User object'''
    all_stored_users = storage.all("User").values()
    one_user_obj = [obj.to_dict() for obj in all_stored_users
                   if obj.id == user_id]
    if one_user_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    one_user_obj[0]['name'] = request.json['name']
    for obj in all_stored_users:
        if obj.id == user_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(one_user_obj[0]), 200
