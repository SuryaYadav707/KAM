from app.models import db, Lead, User
from flask import jsonify

class LeadService:
    @staticmethod
    def create_lead(data):
        try:
            # Fetch KAM by name
            kam = User.query.filter_by(username=data['assigned_kam'], role='Kam').first()
            if not kam:
                return jsonify({'error': 'KAM not found'}), 404

            lead = Lead(
                restaurant_name=data['restaurant_name'],
                address=data['address'],
                contact_number=data['contact_number'],
                status=data['status'],
                assigned_kam=kam
            )
            db.session.add(lead)
            db.session.commit()
            return jsonify({'message': 'Lead created successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

  
        
    @staticmethod
    def update_lead(lead_id, data):
        try:
            lead = Lead.query.get(lead_id)
            if not lead:
                return jsonify({'error': 'Lead not found'}), 404

        # Update fields
            lead.restaurant_name = data.get('restaurant_name', lead.restaurant_name)
            lead.address = data.get('address', lead.address)
            lead.contact_number = data.get('contact_number', lead.contact_number)
            lead.status = data.get('status', lead.status)

        # Update KAM by name if provided
            if 'assigned_kam' in data and data['assigned_kam']:
                kam = User.query.filter_by(username=data['assigned_kam'], role='Kam').first()
                if not kam:
                    return jsonify({'error': 'KAM not found'}), 404
                lead.assigned_kam = kam

            db.session.commit()
            return jsonify({'message': 'Lead updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    

    @staticmethod
    def delete_lead(lead_id):
        try:
            lead = Lead.query.get(lead_id)
            if not lead:
                return jsonify({'error': 'Lead not found'}), 404

            db.session.delete(lead)
            db.session.commit()
            return jsonify({'message': 'Lead deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

   
