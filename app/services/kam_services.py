from app import db
from app.models import User
from bcrypt import hashpw, gensalt

class KamService:
    @staticmethod
    def add_kam(username, password):
        # Check if the KAM user already exists
        existing_kam = User.query.filter_by(username=username).first()
        if existing_kam:
            print(f"KAM with username '{username}' already exists.")
            return None  # KAM already exists

        # Hash the password
        hashed_password = hashpw(password.encode('utf-8'), gensalt())

        # Create new KAM user
        new_kam = User(username=username, password=hashed_password, role='Kam')
        
        try:
            db.session.add(new_kam)
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            print(f"Error during commit: {e}")
            return None

        return {'message': f"KAM user '{username}' created successfully!"}

    @staticmethod
    def search_kams(query):
        return User.query.filter(User.username.ilike(f'%{query}%')).all()

    @staticmethod
    def update_kam(kam_id, username, password):
        kam = User.query.get(kam_id)
        if kam:
            kam.username = username
            if password:
                kam.password = generate_password_hash(password)
            db.session.commit()
            return kam
        return None
