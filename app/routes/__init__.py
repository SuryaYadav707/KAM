# from flask import Blueprint

# # Blueprints for routes
# admin_routes = Blueprint('admin_routes', __name__)
# kam_routes = Blueprint('kam_routes', __name__)
# shared_routes=Blueprint('shared_routes',__name__)
# auth_routest = Blueprint('auth_routes', __name__)

# Import views to register routes
# from . import admin_routes, kam_routes,shared_routes,auth_routes

from .admin_routes import admin_routes
from .kam_routes import kam_routes
from .shared_routes import shared_routes
from .auth_routes import auth_routes

__all__ = ['admin_routes', 'kam_routes', 'shared_routes', 'auth_routes']
