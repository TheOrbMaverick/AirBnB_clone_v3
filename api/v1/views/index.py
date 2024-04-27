#!/usr/bin/python3
""" Doing the index for flask """
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    ''' status page '''
    return jsonify({'status': 'OK'})
