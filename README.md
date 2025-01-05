# README

## Setup Instructions

### Step 1: Create an Environment
To avoid conflicts with existing Python packages, create a new environment using the following command:
```bash
conda create --name kam
```

Activate the environment:
```bash
conda activate kam
```

### Step 2: Install Requirements
Install all required Python packages:
```bash
pip install -r requirements.txt
```

### Step 3: Setup the Database
1. Open MySQL Command Line or Workbench.
2. Run the following commands to create the database and user:
```sql
CREATE DATABASE kam_db;
CREATE USER 'kam_user'@'localhost' IDENTIFIED BY 'kam_pass';
GRANT ALL PRIVILEGES ON kam_db.* TO 'kam_user'@'localhost';
FLUSH PRIVILEGES;
```

### Step 4: Configure the Application
Update the `config.py` file with the following:
```python
SECRET_KEY = "your_sql_password"
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://kam_user:kam_pass@localhost/kam_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
```

### Step 5: Initialize the Database
Run the following commands in your terminal:
```bash
set FLASK_APP=run.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## How to Run the Application

### Step 1: Seed the Admin User
1. Open the `seed_admin.py` file.
2. Update the following variables with your desired admin credentials:
```python
username = "admin_username"
password = "admin_password"
```
3. Run the script:
```bash
python seed_admin.py
```

### Step 2: Start the Application
Run the application using:
```bash
python run.py
```

### Step 3: Seed a KAM User (Optional)
1. Open the `seed_kam_user.py` file.
2. Update the following variables with your desired KAM user credentials:
```python
username = "Kam1"
password = "kam1"
```
3. Run the script:
```bash
python seed_kam_user.py
```

## Access the Application
The application will be running on your local server. Log in as an admin to:
- Add, update, or delete leads.
- Add KAM users.

Congratulations! Your project is set up and running successfully.


# API Documentation

## Authentication Routes

### Login
**Endpoint:** `/login`
**Methods:** `GET`, `POST`

- **GET**: Renders the login page.
- **POST**: Authenticates the user with the provided `username` and `password`.
  - **Request Form Data:**
    - `username`: The username of the user.
    - `password`: The password of the user.
  - **Response:**
    - On success:
      - Redirects to the dashboard based on the user's role (`Admin` or `Kam`).
    - On failure:
      - Renders the login page with an error message.

### Logout
**Endpoint:** `/logout`
**Methods:** `GET`

- Clears the session and redirects to the login page.

### Current User
**Endpoint:** `/current_user`
**Methods:** `GET`

- **Response:**
  - Returns the details of the currently logged-in user.

---

## Admin Routes

### Admin Dashboard
**Endpoint:** `/dashboard`
**Methods:** `GET`, `POST`

- **GET**:
  - Fetches and displays data based on the `lead_or_kam` parameter (`lead` or `kam`).
  - **Query Parameters:**
    - `lead_or_kam`: Specifies whether to fetch leads or KAMs. Defaults to `kam`.
  - **Response:**
    - Renders the admin dashboard with the relevant data.

- **POST**:
  - Handles CRUD operations for leads and contacts.
  - **Request Form Data:**
    - `action`: Specifies the operation (`create_lead`, `update_lead`, `delete_lead`, `create_contact`, `update_contact`, `delete_contact`).
    - Additional fields based on the action.

### Admin Dashboard (KAM)
**Endpoint:** `/dashboard/kam`
**Methods:** `GET`, `POST`

- **GET**:
  - Fetches all KAM users.
  - **Response:**
    - Renders the admin dashboard for KAMs.

- **POST**:
  - Handles CRUD operations for KAMs.
  - **Request Form Data:**
    - `action`: Specifies the operation (`create_kam`).
    - Additional fields based on the action.

### Lead Contacts
**Endpoint:** `/lead_contacts/<int:lead_id>`
**Methods:** `GET`

- **GET**:
  - Fetches contacts associated with a specific lead.
  - **Response:**
    - On success:
      - Returns a list of contacts.
    - On failure:
      - Returns an error message.

### Lead Details
**Endpoint:** `/lead_details/<int:lead_id>`
**Methods:** `GET`

- **GET**:
  - Fetches details of a specific lead, including contacts and interactions.
  - **Response:**
    - On success:
      - Returns lead details.
    - On failure:
      - Returns an error message.

---

## KAM Routes

### KAM Dashboard
**Endpoint:** `/dashboard`
**Methods:** `GET`, `POST`

- **GET**:
  - Fetches leads assigned to the logged-in KAM.
  - **Response:**
    - Renders the KAM dashboard with the relevant data.

- **POST**:
  - Handles adding interactions for leads.
  - **Request Form Data:**
    - `action`: Specifies the operation (`add_interaction`).
    - Additional fields based on the action.

### Lead Details (KAM)
**Endpoint:** `/lead_details/<int:lead_id>`
**Methods:** `GET`

- **GET**:
  - Fetches details of a specific lead, including contacts and interactions.
  - **Response:**
    - On success:
      - Returns lead details.
    - On failure:
      - Returns an error message.

---

## Shared Routes

### Home
**Endpoint:** `/`
**Methods:** `GET`

- **GET**:
  - Renders the home page.

---






# Database Design for KAM Functionality

## Tables and Relationships

### 1. **Users Table** (`users`)
| Column Name | Data Type    | Constraints                       |
|-------------|--------------|-----------------------------------|
| id          | Integer      | Primary Key                      |
| username    | String(80)   | Unique, Not Null                 |
| password    | String(200)  | Not Null                         |
| role        | String(20)   | Not Null (Values: Admin, KAM)    |

### 2. **Leads Table** (`leads`)
| Column Name        | Data Type    | Constraints                       |
|--------------------|--------------|-----------------------------------|
| id                 | Integer      | Primary Key                      |
| restaurant_name    | String(100)  | Not Null, Unique                 |
| address            | String(200)  | Not Null                         |
| contact_number     | String(15)   | Not Null                         |
| status             | String(20)   | Not Null (Values: New, Active, Inactive) |
| assigned_kam_id    | Integer      | Foreign Key (`users.id`)         |

**Relationships:**
- `assigned_kam` is a foreign key relationship with the `users` table.
- One-to-many relationship: A user (KAM) can have multiple leads.
- Cascade delete orphan behavior for related `contacts` and `interactions`.

### 3. **Contacts Table** (`contacts`)
| Column Name   | Data Type    | Constraints                       |
|---------------|--------------|-----------------------------------|
| id            | Integer      | Primary Key                      |
| name          | String(100)  | Not Null                         |
| role          | String(50)   | Not Null (e.g., Owner, Manager)  |
| phone_number  | String(15)   | Not Null                         |
| email         | String(254)  | Not Null                         |
| lead_id       | Integer      | Foreign Key (`leads.id`), Not Null |

**Relationships:**
- `lead_id` links to the `leads` table.
- One-to-many relationship: A lead can have multiple contacts.

### 4. **Interactions Table** (`interactions`)
| Column Name        | Data Type    | Constraints                       |
|--------------------|--------------|-----------------------------------|
| id                 | Integer      | Primary Key                      |
| date               | Date         | Not Null                         |
| interaction_type   | String(20)   | Not Null (Values: Call, Visit, Order) |
| notes              | Text         | Optional                         |
| follow_up_required | Boolean      | Default: False                   |
| lead_id            | Integer      | Foreign Key (`leads.id`)         |
| kam_id             | Integer      | Foreign Key (`users.id`)         |

**Relationships:**
- `lead_id` links to the `leads` table.
- `kam_id` links to the `users` table.
- One-to-many relationship: A lead can have multiple interactions.
- One-to-many relationship: A KAM can have multiple interactions.

## Entity-Relationship (ER) Diagram

```plaintext
Users (id, username, password, role)
    |
    |<-- assigned_kam_id
    |
Leads (id, restaurant_name, address, contact_number, status, assigned_kam_id)
    |
    |<-- lead_id
    |
Contacts (id, name, role, phone_number, email, lead_id)
    |
    |<-- lead_id, kam_id
    |
Interactions (id, date, interaction_type, notes, follow_up_required, lead_id, kam_id)
```

## Notes
1. **Normalization:**
   - The design ensures proper normalization with no data redundancy.
   - Foreign keys maintain referential integrity.

2. **Constraints:**
   - Use constraints like `NOT NULL`, `UNIQUE`, and `DEFAULT` to ensure data consistency.

3. **Relationships:**
   - Cascading deletes for `contacts` and `interactions` ensure cleanup of related data when a lead is removed.
