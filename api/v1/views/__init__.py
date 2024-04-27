from flask import Blueprint
from api.v1.views.index import *
""" Using flask Blueprint """

# Create a Blueprint instance with a URL prefix of '/api/v1'
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
