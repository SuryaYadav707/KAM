from app import app as  create_app, db
from app.models import User
from bcrypt import gensalt, hashpw

# Create and seed a KAM user
def seed_kam_user():
    app = create_app()
    with app.app_context():
        username = "Kam1"
        password = "kam1"

        # Check if KAM user already exists
        if not User.query.filter_by(username=username).first():
            # Hash the password
            hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
            
            # Create the KAM user with hashed password
            kam_user = User(username=username, password=hashed_password, role="Kam")
            db.session.add(kam_user)
            db.session.commit()
            print(f"KAM user '{username}' created successfully!")
        else:
            print("KAM user already exists.")

if __name__ == "__main__":
    seed_kam_user()
