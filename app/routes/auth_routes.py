from flask import Blueprint, redirect, request, render_template, session, url_for
from app.services.auth_services import AuthService
import logging

logging.basicConfig(level=logging.DEBUG)

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    # Clear any existing session data before login
    session.clear()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        logging.debug(f"Login attempt with username: {username}")

        response, status_code = AuthService.login(username, password)
        if status_code == 200:
            user_data = response.get_json()
            
            # Set session data based on the role
            session['role'] = user_data['role']
            session['user_id'] = user_data['id']

            if user_data['role'] == 'Kam':
                session['kam_id'] = user_data['id']  # Only set if the role is Kam

            logging.debug(f"Session data after login: {session}")

            # Redirect based on the role
            if user_data['role'] == 'Admin':
                logging.debug("Admin logged in, redirecting to admin dashboard.")
                return redirect(url_for('admin_routes.admin_dashboard'))
            elif user_data['role'] == 'Kam':
                logging.debug("Kam logged in, redirecting to Kam dashboard.")
                return redirect(url_for('kam_routes.kam_dashboard'))
        else:
            # Handle login error
            error_message = response.get_json().get('error')
            logging.error(f"Login failed: {error_message}")
            return render_template('login.html', error=error_message)
    
    return render_template('login.html')

@auth_routes.route('/logout')
def logout():
    AuthService.logout()
    session.clear()
    return redirect(url_for('auth_routes.login'))


@auth_routes.route('/current_user', methods=['GET'])
def current_user():
    user = AuthService.get_current_user()
    logging.debug(f"Current user fetched: {user}")
    return user
