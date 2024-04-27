from flask import jsonify
from . import app_views

# Define a route /status on the app_views Blueprint
@app_views.route('/status', methods=['GET'])
def get_status():
    """Return a JSON response with status 'OK'"""
    return jsonify({'status': 'OK'})