from app import app as create_app, db
from app.models import User
from bcrypt import gensalt, hashpw

# Create and seed an admin user
def seed_admin_user():
    app = create_app()
    with app.app_context():
        username = "admin_username"
        password = "admin_password"

        # Check if admin already exists
        if not User.query.filter_by(username=username).first():
            # Hash the password
            hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
            
            # Create the admin user with hashed password
            admin_user = User(username=username, password=hashed_password, role="Admin")
            db.session.add(admin_user)
            db.session.commit()
            print(f"Admin user '{username}' created successfully!")
        else:
            print("Admin user already exists.")

if __name__ == "__main__":
    seed_admin_user()
