import logging
from flask import jsonify, session
from app.models import User
from bcrypt import checkpw, gensalt, hashpw

logging.basicConfig(level=logging.DEBUG)

class AuthService:
    @staticmethod
    def hash_password(password):
        return hashpw(password.encode('utf-8'), gensalt())

    @staticmethod
    def login(username, password):
        logging.debug(f"Login attempt with username: {username}")
        try:
            # Fetch user by username
            user = User.query.filter_by(username=username).first()
            if not user:
                logging.error("User not found.")
                return jsonify({'error': 'Invalid username or password'}), 401

            # Verify password
            if not checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                logging.error("Password mismatch.")
                return jsonify({'error': 'Invalid username or password'}), 401

            logging.debug(f"User authenticated: {user.username} with role {user.role}")
            return jsonify({'id': user.id, 'role': user.role, 'username': user.username}), 200
        except Exception as e:
            logging.error(f"Error during login: {e}")
            return jsonify({'error': 'An error occurred during login'}), 500

    @staticmethod
    def logout():
        logging.debug("User logged out.")

    @staticmethod
    def get_current_user(session):
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not logged in'}), 401

        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({'id': user.id, 'role': user.role, 'username': user.username}), 200


    @staticmethod
    def check_admin_permission():
        """ Ensure that the logged-in user is an admin """
        user_id = session.get('user_id')
        if not user_id:
            return False

        user = User.query.get(user_id)
        if not user or user.role != 'Admin':
            return False

        return True
