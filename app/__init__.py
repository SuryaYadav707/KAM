from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes import admin_routes, kam_routes, shared_routes, auth_routes
    app.register_blueprint(admin_routes, url_prefix='/admin_routes')
    app.register_blueprint(kam_routes, url_prefix='/kam_routes')
    app.register_blueprint(shared_routes)
    app.register_blueprint(auth_routes, url_prefix='/auth_routes')

    with app.app_context():
        from app.models import User, Lead, Contact, Interaction
        db.create_all()

    return app
