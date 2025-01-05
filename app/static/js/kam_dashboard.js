function openInteractionModal(leadId, interactionType = 'Call', interactionDate = '', notes = '', followUpRequired = false) {
    document.getElementById('lead_id').value = leadId || '';
    document.getElementById('interaction_type').value = interactionType || 'Call';  // Default to 'call' if no type is provided
    document.getElementById('interaction_date').value = interactionDate || '';
    document.getElementById('notes').value = notes || '';
    document.getElementById('follow_up_required').checked = followUpRequired;  // This will check or uncheck the checkbox

    document.getElementById('action').value = 'add_interaction';  // Set the action field
}

// Function to submit the interaction form
function submitInteractionForm() {
    const formData = new FormData(document.getElementById('interactionForm'));

    // Ensure follow_up_required is set to 0 if not checked
    if (!document.getElementById('follow_up_required').checked) {
        formData.set('follow_up_required', '0');
    }

    fetch('/kam_routes/dashboard', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || 'Interaction added');
        location.reload();  // Reload the page to update the leads list
    })
    .catch(err => console.error('Error submitting interaction:', err));
}

// Function to fetch and display lead details in the modal
function viewLeadDetails(leadId) {
    fetch(`/kam_routes/lead_details/${leadId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                const lead = data.lead;

                // Create HTML content for lead details
                let detailsHTML = `
                    <h5>Restaurant Name: ${lead.restaurant_name}</h5>
                    <p><strong>Status:</strong> ${lead.status}</p>
                    <p><strong>Address:</strong> ${lead.address}</p>
                    <p><strong>Contact Number:</strong> ${lead.contact_number}</p>
                    <p><strong>Assigned KAM:</strong> ${lead.assigned_kam || 'Not Assigned'}</p>
                    <h6>Contacts:</h6>
                    <ul>
                `;

                lead.contacts.forEach(contact => {
                    detailsHTML += `
                        <li><strong>${contact.name}</strong> (${contact.role}) - ${contact.phone_number}, ${contact.email}</li>
                    `;
                });

                detailsHTML += '</ul><h6>Interactions:</h6><ul>';

                lead.interactions.forEach(interaction => {
                    detailsHTML += `
                        <li><strong>${interaction.interaction_type}</strong> on ${interaction.interaction_date}
                            <br>Notes: ${interaction.notes} 
                            <br>Follow-up Required: ${interaction.follow_up_required ? 'Yes' : 'No'}</li>
                    `;
                });

                detailsHTML += '</ul>';

                // Insert the details into the modal content
                const leadDetailsContent = document.getElementById('leadDetailsContent');
                leadDetailsContent.innerHTML = detailsHTML;

                // Show the modal with lead details
                // new bootstrap.Modal(document.getElementById('leadDetailsModal')).show();
            }
        })
        .catch(err => console.error('Error fetching lead details:', err));
}

// Function to filter leads based on search and status
function filterLeads() {
    const searchRestaurant = document.getElementById('searchRestaurant').value.toLowerCase();
    const filterStatus = document.getElementById('filterStatus').value.toLowerCase();

    const leads = document.querySelectorAll('.lead-item');
    let hasResults = false;

    leads.forEach(lead => {
        const restaurant = lead.getAttribute('data-restaurant') || '';
        const status = lead.getAttribute('data-status') || '';

        if ((restaurant.includes(searchRestaurant) || searchRestaurant === '') &&
            (status.includes(filterStatus) || filterStatus === '')) {
            lead.style.display = 'block';
            hasResults = true;
        } else {
            lead.style.display = 'none';
        }
    });

    // Show or hide the "No Results" message
    const noResultsDiv = document.getElementById('noResults');
    if (hasResults) {
        noResultsDiv.style.display = 'none';
    } else {
        noResultsDiv.style.display = 'block';
    }
}