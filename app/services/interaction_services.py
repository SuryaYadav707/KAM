from app.models import db, Interaction, Lead, User
from flask import jsonify
from datetime import datetime

class InteractionService:
    @staticmethod
    def log_interaction(data):
        try:
            # Parse the date from the form (assuming it's in 'YYYY-MM-DD' format)
            interaction_date = datetime.strptime(data['date'], '%Y-%m-%d')

            interaction = Interaction(
                date=interaction_date,
                interaction_type=data['interaction_type'],
                notes=data['notes'],
                follow_up_required=data['follow_up_required'],
                lead_id=data['lead_id'],
                kam_id=data['kam_id']
            )
            db.session.add(interaction)
            db.session.commit()

            return jsonify({'message': 'Interaction logged successfully'}), 201
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            print(f"Error logging interaction: {e}")
            return jsonify({'error': 'An error occurred while logging the interaction'}), 500



    @staticmethod
    def get_interactions(admin_view=False, kam_id=None):
        """Retrieve interactions along with associated contact details."""
        if admin_view:
            interactions = Interaction.query.all()
        elif kam_id:
            interactions = Interaction.query.filter_by(kam_id=kam_id).all()
        else:
            return jsonify({'error': 'Unauthorized access'}), 403

        return jsonify([{
            'id': interaction.id,
            'date': interaction.date,
            'type': interaction.interaction_type,
            'notes': interaction.notes,
            'follow_up_required': interaction.follow_up_required,
            'restaurant_name': interaction.lead.restaurant_name if interaction.lead else None,
            'contacts': [{
                'id': contact.id,
                'name': contact.name,
                'role': contact.role,
                'phone_number': contact.phone_number,
                'email': contact.email
            } for contact in interaction.lead.contacts] if interaction.lead else []  # Include contacts if a lead exists
        } for interaction in interactions]), 200


    @staticmethod
    def search_interactions(query, admin_view=False, kam_id=None):
        """Search interactions by follow-up status or restaurant name."""
        search_query = f"%{query}%"
        if admin_view:
            interactions = Interaction.query.filter(
                (Interaction.follow_up_required == (query.lower() == "yes")) |
                (Interaction.lead.has(Lead.restaurant_name.ilike(search_query)))
            ).all()
        elif kam_id:
            interactions = Interaction.query.filter(
                (Interaction.kam_id == kam_id) & 
                (Interaction.lead.has(Lead.restaurant_name.ilike(search_query)))
            ).all()
        else:
            return jsonify({'error': 'Unauthorized access'}), 403

        return jsonify([{
            'id': interaction.id,
            'date': interaction.date,
            'type': interaction.interaction_type,
            'notes': interaction.notes,
            'follow_up_required': interaction.follow_up_required,
            'restaurant_name': interaction.lead.restaurant_name if interaction.lead else None,
            'contacts': [{
                'id': contact.id,
                'name': contact.name,
                'role': contact.role,
                'phone_number': contact.phone_number,
                'email': contact.email
            } for contact in interaction.lead.contacts] if interaction.lead else []  # Include contacts if a lead exists
        } for interaction in interactions]), 200
