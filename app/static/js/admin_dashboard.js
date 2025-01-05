function openLeadModal(id = null, name = '', status = 'new', address = '', contact = '', assigned_kam = '') {
    document.getElementById('lead_id').value = id || '';
    document.getElementById('restaurant_name').value = name || '';
    document.getElementById('address').value = address || '';
    document.getElementById('contact_number').value = contact || '';
    document.getElementById('status').value = status || 'new';
    document.getElementById('assigned_kam').value = assigned_kam || '';
    document.getElementById('action').value = id ? 'update_lead' : 'create_lead';
}

function submitLeadForm() {
    const formData = new FormData(document.getElementById('leadForm'));
    fetch('/admin_routes/dashboard', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || 'Action completed');
        location.reload();
    })
    .catch(err => console.error(err));
}

function openContactModal(leadId) {
    document.getElementById('contact_lead_id').value = leadId;

    fetch(`/admin_routes/lead_contacts/${leadId}`)
        .then(response => response.json())
        .then(data => {
            const contactListDiv = document.getElementById('contactList');
            contactListDiv.innerHTML = '';

            data.contacts.forEach(contact => {
                contactListDiv.innerHTML += `
                    <div class="contact-item mb-2">
                        <span><strong>${contact.name}</strong> (${contact.role})</span>
                        <button class="btn btn-warning" onclick="openContactForm('update', ${leadId}, ${contact.id}, '${contact.name}', '${contact.role}', '${contact.phone_number}', '${contact.email}')">Update</button>
                        <button class="btn btn-danger" onclick="deleteContact(${contact.id})">Delete</button>
                    </div>
                `;
            });
        })
        .catch(err => console.error('Error fetching contacts:', err));
}

function openContactForm(action, leadId, contactId = null, name = '', role = '', phoneNumber = '', email = '') {
    document.getElementById('contact_action').value = action === 'add' ? 'create_contact' : 'update_contact';
    document.getElementById('contact_lead_id').value = leadId || '';
    document.getElementById('contact_id').value = contactId || '';

    if (action === 'update') {
        document.getElementById('name').value = name;
        document.getElementById('role').value = role;
        document.getElementById('phone_number').value = phoneNumber;
        document.getElementById('email').value = email;
    } else {
        document.getElementById('name').value = '';
        document.getElementById('role').value = '';
        document.getElementById('phone_number').value = '';
        document.getElementById('email').value = '';
    }

    // Open the contact form modal
    new bootstrap.Modal(document.getElementById('contactFormModal')).show();
}

function submitContactForm() {
    const formData = new FormData(document.getElementById('contactForm'));
    const action = document.getElementById('contact_action').value;
    formData.append('action', action);

    fetch('/admin_routes/dashboard', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message); // Success message from the backend
            document.getElementById('contactFormContainer').style.display = 'none';
            location.reload();
        } else if (data.error) {
            alert(data.error); // Error message from the backend
        }
    })
    .catch(err => console.error('Error:', err));
}

function deleteLead(id) {
    if (confirm('Are you sure you want to delete this lead?')) {
        fetch('/admin_routes/dashboard', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `action=delete_lead&lead_id=${id}`
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || 'Lead deleted');
            location.reload();
        })
        .catch(err => console.error(err));
    }
}

function deleteContact(id) {
    if (confirm('Are you sure you want to delete this contact?')) {
        fetch(`/admin_routes/delete_contact/${id}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || 'Contact deleted');
            location.reload();
        })
        .catch(err => console.error(err));
    }
}

function viewLeadDetails(leadId) {
    fetch(`/admin_routes/lead_details/${leadId}`)
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
                new bootstrap.Modal(document.getElementById('leadDetailsModal')).show();
            }
        })
        .catch(err => console.error('Error fetching lead details:', err));
}

// function filterLeads() {
//     const searchKam = document.getElementById('searchKam').value.toLowerCase();
//     const searchRestaurant = document.getElementById('searchRestaurant').value.toLowerCase();
//     const filterStatus = document.getElementById('filterStatus').value;

//     const leads = document.querySelectorAll('.lead-item');
//     let hasResults = false;

//     leads.forEach(lead => {
//         const kam = lead.getAttribute('data-kam').toLowerCase();
//         const restaurant = lead.getAttribute('data-restaurant').toLowerCase();
//         const status = lead.getAttribute('data-status');

//         if ((kam.includes(searchKam) || searchKam === '') &&
//             (restaurant.includes(searchRestaurant) || searchRestaurant === '') &&
//             (status.includes(filterStatus) || filterStatus === '')) {
//             lead.style.display = 'block';
//             hasResults = true;
//         } else {
//             lead.style.display = 'none';
//         }
//     });

//     // Show or hide the "No Results" message
//     const noResultsDiv = document.getElementById('noResults');
//     if (hasResults) {
//         noResultsDiv.style.display = 'none';
//     } else {
//         noResultsDiv.style.display = 'block';
//     }
// }

// function fetchDashboard(selectedType) {
//         console.log("Selected Type:", selectedType);

//         fetch('/admin_routes/dashboard', {
//             method: 'GET',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'Selected-Type': selectedType // Custom header to pass selected type
//             }
//         })
//         .then(response => {
//             console.log('Raw Response:', response);
//             if (!response.ok) {
//                 throw new Error(`HTTP error! Status: ${response.status}`);
//             }
//             return response.text(); // Temporarily use text() to inspect the raw response
//         })
//         .then(text => {
//             console.log('Raw Response Text:', text);
//             const data = JSON.parse(text); // Convert back to JSON if it is valid
//             console.log('Dashboard Data:', data);
//             const dashboard = document.getElementById('dashboard');
//             dashboard.innerHTML = JSON.stringify(data, null, 2);
//         })
//         .catch(error => {
//             console.error('Error fetching dashboard data:', error);
//         });
//     }

// Handle Type Toggle (Lead/KAM)
// Handle Type Toggle (Lead/KAM)

// 

function toggleRoute(type) {
    // Construct the URL with the correct prefix
    const baseUrl = '/admin_routes/dashboard';
    const url = type === 'lead' ? `${baseUrl}` : `${baseUrl}/kam`;
    
    // Redirect to the constructed URL
    window.location.href = url;
}



  


// Initialize the page to show the appropriate button and list based on the initial state
window.onload = function() {
    // Default type should be "lead"
    toggleType('lead');
};




// Filter Leads/KAMs Based on Search Inputs
function filterLeads() {
    const searchKam = document.getElementById('searchKam').value.toLowerCase();
    const searchRestaurant = document.getElementById('searchRestaurant').value.toLowerCase();
    const filterStatus = document.getElementById('filterStatus').value.toLowerCase();

    // Select all lead/KAM items
    const leadItems = document.querySelectorAll('.lead-item');
    const kamItems = document.querySelectorAll('.kam-item');

    // Determine the selected type (Lead or KAM)
    const isLeadSelected = document.getElementById('leadToggle').checked;

    let foundResults = false;

    if (isLeadSelected) {
        // Filter Leads
        leadItems.forEach(item => {
            const kam = item.getAttribute('data-kam').toLowerCase();
            const restaurant = item.getAttribute('data-restaurant').toLowerCase();
            const status = item.getAttribute('data-status').toLowerCase();

            if (
                (kam.includes(searchKam) || searchKam === '') &&
                (restaurant.includes(searchRestaurant) || searchRestaurant === '') &&
                (status.includes(filterStatus) || filterStatus === '')
            ) {
                item.style.display = '';
                foundResults = true;
            } else {
                item.style.display = 'none';
            }
        });

        // Hide all KAM items
        kamItems.forEach(item => {
            item.style.display = 'none';
        });
    } else {
        // Filter KAMs
        kamItems.forEach(item => {
            const username = item.getAttribute('data-username').toLowerCase();

            if (username.includes(searchKam) || searchKam === '') {
                item.style.display = '';
                foundResults = true;
            } else {
                item.style.display = 'none';
            }
        });

        // Hide all Lead items
        leadItems.forEach(item => {
            item.style.display = 'none';
        });
    }

    // Show 'No Results' message if no results are found
    const noResults = document.getElementById('noResults');
    if (!foundResults) {
        noResults.style.display = 'block';
    } else {
        noResults.style.display = 'none';
    }
}




// Open KAM Modal for Updating KAM Details
function openKamModal(kamId = null, username = '',password='') {
    document.getElementById('kamForm').reset();
    document.getElementById('kam_id').value = kamId || '';
    document.getElementById('kam_username').value = username;
    document.getElementById('kam_password').value=password;
    document.getElementById('action').value = kamId ? 'update_kam' : 'create_kam';

}

// Submit KAM Form (Update KAM)
function submitKamForm() {
    const formData = new FormData(document.getElementById('kamForm'));
   
        fetch('/admin_routes/dashboard', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || 'Action completed');
        location.reload();
    })
    .catch(err => console.error(err));
}
