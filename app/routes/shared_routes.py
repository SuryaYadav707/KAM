from flask import Blueprint, jsonify, render_template, request, session

shared_routes = Blueprint('shared_routes', __name__)

@shared_routes.route('/', methods=['GET'])
def home():
    """Render the home page."""
    return render_template('home.html')

