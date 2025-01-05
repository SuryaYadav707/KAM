from app.models import db, Contact, Lead
from flask import jsonify

class ContactService:
    
    @staticmethod
    def create_contact(data):
        if not all([data.get('lead_id'), data.get('name'), data.get('role'), data.get('phone_number'), data.get('email')]):
            return jsonify({'error': 'Missing required fields'}), 400

        lead_id = data.get('lead_id')
        name = data.get('name')
        role = data.get('role')
        phone_number = data.get('phone_number')
        email = data.get('email')

        contact = Contact(
            lead_id=lead_id,
            name=name,
            role=role,
            phone_number=phone_number,
            email=email
        )
        db.session.add(contact)
        db.session.commit()

        # Return updated contact list
        lead = Lead.query.get(lead_id)
        contacts_data = [
            {
                'id': contact.id,
                'name': contact.name,
                'role': contact.role,
                'phone_number': contact.phone_number,
                'email': contact.email
            } for contact in lead.contacts
        ]
        return jsonify({'message': 'Contact added successfully', 'contacts': contacts_data})

    @staticmethod
    def update_contact(contact_id, data):
        contact = Contact.query.get(contact_id)
        if not contact:
            return jsonify({'error': 'Contact not found'}), 404

        if not all([data.get('name'), data.get('role'), data.get('phone_number'), data.get('email')]):
            return jsonify({'error': 'Missing required fields for contact update'}), 400

        try:
            contact.name = data.get('name')
            contact.role = data.get('role')
            contact.phone_number = data.get('phone_number')
            contact.email = data.get('email')
            db.session.commit()

            lead = contact.lead
            contacts_data = [
                {
                    'id': c.id,
                    'name': c.name,
                    'role': c.role,
                    'phone_number': c.phone_number,
                    'email': c.email
                } for c in lead.contacts
            ]
            return jsonify({'message': 'Contact updated successfully', 'contacts': contacts_data})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to update contact: {str(e)}'}), 500


    @staticmethod
    def delete_contact(contact_id):
        contact = Contact.query.get(contact_id)
        if contact:
            lead_id = contact.lead_id
            db.session.delete(contact)
            db.session.commit()

            # Return updated contact list
            lead = Lead.query.get(lead_id)
            contacts_data = [
                {
                    'id': contact.id,
                    'name': contact.name,
                    'role': contact.role,
                    'phone_number': contact.phone_number,
                    'email': contact.email
                } for contact in lead.contacts
            ]
            return jsonify({'message': 'Contact deleted successfully', 'contacts': contacts_data})
        return jsonify({'error': 'Contact not found'}), 404
    
    @staticmethod
    def get_contact(contact_id):
        contact = Contact.query.get(contact_id)
        if contact:
            contact_data = {
                'id': contact.id,
                'name': contact.name,
                'role': contact.role,
                'phone_number': contact.phone_number,
                'email': contact.email
            }
            return jsonify({'contact': contact_data})
        return jsonify({'error': 'Contact not found'}), 404