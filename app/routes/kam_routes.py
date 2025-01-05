from flask import Blueprint, redirect, request, jsonify, render_template, session, url_for
from app.models import Lead
from app.services.interaction_services import InteractionService  # Import the InteractionService

kam_routes = Blueprint('kam_routes', __name__)

@kam_routes.route('/dashboard', methods=['GET', 'POST'])
def kam_dashboard():
    print("Raw form data:", request.form.to_dict())

    # Get the logged-in KAM's ID from the session
    kam_id = session.get('user_id')  # Ensure the KAM's ID is stored in session when they log in
    if not kam_id:
        return redirect(url_for('auth_routes.login'))  # Redirect to login if the KAM is not logged in

    if request.method == 'GET':
        # Fetch data for the logged-in KAM
        leads = Lead.query.filter_by(assigned_kam_id=kam_id).all()
        total_leads = len(leads)

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
        return render_template('kam_dashboard.html', leads=leads_data, total_leads=total_leads)

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add_interaction':
            # Add interaction logic
            lead_id = request.form.get('lead_id')
            interaction_type = request.form.get('interaction_type')
            interaction_date = request.form.get('interaction_date')
            notes = request.form.get('notes')
            follow_up_required = 'follow_up_required' in request.form

            # Prepare interaction data
            interaction = {
                'date': interaction_date,
                'interaction_type': interaction_type,
                'notes': notes,
                'follow_up_required': follow_up_required,
                'lead_id': lead_id,
                'kam_id': kam_id
            }

            # Call the service to log the interaction
            return InteractionService.log_interaction(interaction)

        return jsonify({'error': 'Invalid action'}), 400


@kam_routes.route('/lead_details/<int:lead_id>', methods=['GET'])
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
                    'interaction_date': interaction.date,  # Use date here
                    'interaction_type': interaction.interaction_type,
                    'notes': interaction.notes,
                    'follow_up_required': interaction.follow_up_required
                } for interaction in interactions
            ]
        }

        return jsonify({'lead': lead_data}), 200

    except Exception as e:
        kam_routes.logger.error(f"Error fetching details for lead {lead_id}: {e}")
        return jsonify({'error': 'An error occurred while fetching lead details'}), 500