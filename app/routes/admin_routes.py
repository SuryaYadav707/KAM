from flask import Blueprint, request, jsonify, render_template
from app.models import Lead, User
from app.services.lead_services import LeadService
from app.services.contact_services import ContactService
from app.services.kam_services import KamService

admin_routes = Blueprint('admin_routes', __name__)

@admin_routes.route('/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    print("Raw form data:", request.form.to_dict())
      
    if request.method == 'GET':
        selected_type = request.args.get('lead_or_kam', 'kam')
        print("Selected type received from frontend:", selected_type)
        

        # Fetch total leads and KAMs
        total_leads = Lead.query.count()
        total_kams = User.query.filter_by(role='Kam').count()

        print("Selected type:", selected_type)


        # If 'lead' is selected, fetch leads
        leads = Lead.query.all()
        leads_data = [
                {
                    'id': lead.id,
                    'restaurant_name': lead.restaurant_name,
                    'status': lead.status,
                    'address': lead.address,
                    'contact_number': lead.contact_number,
                    'assigned_kam': lead.assigned_kam.username if lead.assigned_kam else None,
                    'contacts': [
                        {
                            'id': contact.id,
                            'name': contact.name,
                            'role': contact.role,
                            'phone_number': contact.phone_number,
                            'email': contact.email
                        } for contact in lead.contacts
                    ]
                }
                for lead in leads
            ]
        return render_template('admin_dashboard.html', leads=leads_data, total_leads=total_leads, total_kams=total_kams, selected_type='lead')

        # If 'kam' is selected, fetch KAM users
        

    if request.method == 'POST':
        data = request.form.to_dict()
        print("Parsed form data:", data)
        action = data.get('action')

        if action == 'create_lead':
            lead_data = {
                'restaurant_name': request.form.get('restaurant_name'),
                'contact_number': request.form.get('contact_number'),
                'address': request.form.get('address'),
                'status': request.form.get('status'),
                'assigned_kam': request.form.get('assigned_kam')
            }
            return LeadService.create_lead(lead_data)

        elif action == 'update_lead':
            lead_id = request.form.get('lead_id')
            lead_data = {
                'restaurant_name': request.form.get('restaurant_name'),
                'contact_number': request.form.get('contact_number'),
                'address': request.form.get('address'),
                'status': request.form.get('status'),
                'assigned_kam': request.form.get('assigned_kam')
            }
            return LeadService.update_lead(lead_id, lead_data)

        elif action == 'delete_lead':
            lead_id = request.form.get('lead_id')
            return LeadService.delete_lead(lead_id)

        elif action == 'create_contact':
            return ContactService.create_contact(data)

        elif action == 'update_contact':
            contact_id = data.get('contact_id')

            if not contact_id:
                return jsonify({'error': 'Contact ID is required for update'}), 400

            return ContactService.update_contact(contact_id, data)

        elif action == 'delete_contact':
            contact_id = data.get('contact_id')

            if not contact_id:
                return jsonify({'error': 'Contact ID is required for deletion'}), 400

            return ContactService.delete_contact(contact_id)
        
        
        
@admin_routes.route('/dashboard/kam', methods=['GET', 'POST'])
def admin_dashboard_kam():
    print("Raw form data:", request.form.to_dict())
      
    if request.method == 'GET': 

        # Fetch total leads and KAMs
        total_leads = Lead.query.count()
        total_kams = User.query.filter_by(role='Kam').count()

        # If 'lead' is selected, fetch lead

        # If 'kam' is selected, fetch KAM users
        kams = User.query.filter_by(role='Kam').all()
        kams_data = [
                {
                    'id': kam.id,
                    'username': kam.username,
                    'password': kam.password
                } for kam in kams
            ]
        print("KAMs Data:", kams_data)

        return render_template('admin_dashboard_kam.html', kams=kams_data, total_leads=total_leads, total_kams=total_kams, selected_type='kam')

    if request.method == 'POST':
        data = request.form.to_dict()
        print("Parsed form data:", data)
        action = data.get('action')

        if action == 'create_kam':
            username = request.form.get('username')
            password = request.form.get('password')
            kam = KamService.add_kam(username, password)
            if kam:
                response = jsonify({'message': f"KAM user '{username}' created successfully!"})
                response.status_code = 200
                return response
            else:
                response = jsonify({'error': 'KAM already exists'})
                response.status_code = 400
                return response

        elif action == 'update_kam':
            kam_id = request.form.get('kam_id')
            username = request.form.get('username')
            password = request.form.get('password')
            kam = KamService.update_kam(kam_id, username, password)
            if kam:
                return jsonify({'message': 'KAM updated successfully'}), 200
            else:
                return jsonify({'error': 'Failed to update KAM'}), 400

        else:
            return jsonify({'error': 'Invalid action'}), 400


@admin_routes.route('/lead_contacts/<int:lead_id>', methods=['GET'])
def get_lead_contacts(lead_id):
    try:
        # Fetch the lead
        lead = Lead.query.get(lead_id)
        if not lead:
            return jsonify({'error': 'Lead not found'}), 404

        # Fetch associated contacts
        contacts = lead.contacts

        # If no contacts, return a message
        if not contacts:
            return jsonify({'message': 'No contacts found for this lead'}), 200

        # Prepare the contacts data
        contacts_data = [
            {
                'id': contact.id,
                'name': contact.name,
                'role': contact.role,
                'phone_number': contact.phone_number,
                'email': contact.email
            } for contact in contacts
        ]

        # Return the contacts data
        return jsonify({'contacts': contacts_data}), 200

    except Exception as e:
        # Log the error and return a generic error message
        admin_routes.logger.error(f"Error fetching contacts for lead {lead_id}: {e}")
        return jsonify({'error': 'An error occurred while fetching contacts'}), 500
    
@admin_routes.route('/lead_details/<int:lead_id>', methods=['GET'])
def get_lead_details(lead_id):
    try:
        # Fetch the lead by its ID
        lead = Lead.query.get(lead_id)
        if not lead:
            return jsonify({'error': 'Lead not found'}), 404

        # Fetch associated contacts
        contacts = lead.contacts

        # Fetch associated interactions
        interactions = lead.interactions

        # Prepare the lead data
        lead_data = {
            'id': lead.id,
            'restaurant_name': lead.restaurant_name,
            'status': lead.status,
            'address': lead.address,
            'contact_number': lead.contact_number,
            'assigned_kam': lead.assigned_kam.username if lead.assigned_kam else None,
            'contacts': [
                {
                    'id': contact.id,
                    'name': contact.name,
                    'role': contact.role,
                    'phone_number': contact.phone_number,
                    'email': contact.email
                } for contact in contacts
            ],
            'interactions': [
                {
                    'id': interaction.id,
                    'interaction_date': interaction.date,  # Use `date` here
                    'interaction_type': interaction.interaction_type,
                    'notes': interaction.notes,
                    'follow_up_required': interaction.follow_up_required
                } for interaction in interactions
            ]
        }

        return jsonify({'lead': lead_data}), 200

    except Exception as e:
        admin_routes.logger.error(f"Error fetching details for lead {lead_id}: {e}")
        return jsonify({'error': 'An error occurred while fetching lead details'}), 500
