from app import db 
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Admin or KAM

class Lead(db.Model):
    __tablename__ = 'leads'
    id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String(100), nullable=False)  # Unique Identifier
    address = db.Column(db.String(200), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # New, Active, Inactive
    assigned_kam_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    assigned_kam = db.relationship('User', backref='leads')
    contacts = db.relationship('Contact', backref='lead', cascade="all, delete-orphan")
    interactions = db.relationship('Interaction', backref='lead', cascade="all, delete-orphan")

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # e.g., Owner, Manager
    phone_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(254), nullable=False)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'), nullable=False)

class Interaction(db.Model):
    __tablename__ = 'interactions'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    interaction_type = db.Column(db.String(20), nullable=False)  # Call, Visit, Order
    notes = db.Column(db.Text, nullable=True)
    follow_up_required = db.Column(db.Boolean, default=False)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'))
    kam_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    kam = db.relationship('User', backref='interactions')

