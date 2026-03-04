# Secure Password Manager API

A RESTful API for securely storing and managing passwords, built with Flask and PostgreSQL. Passwords are encrypted at rest using Fernet symmetric encryption, and all endpoints are protected with JWT authentication.

## Live Demo

![Deploy](https://img.shields.io/badge/deployed-railway-blueviolet)

API live at: https://secure-password-manager-production.up.railway.app

> **Note:** This is a demo environment. Do not store real passwords.

## Features

- User registration and login with bcrypt password hashing
- JWT-based authentication with token expiry
- Fernet symmetric encryption for stored passwords
- Full CRUD operations for password entries
- Pagination support on list endpoints
- Rate limiting on authentication endpoints
- Audit logging for all password operations
- Comprehensive test suite with pytest

## Tech Stack

- **Framework:** Flask
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy + Flask-Migrate
- **Authentication:** JWT (Flask-JWT-Extended)
- **Encryption:** Fernet (cryptography)
- **Testing:** pytest

## Getting Started

### Prerequisites
- Python 3.12+
- PostgreSQL

### Installation

1. Clone the repository:
bash
    git clone https://github.com/Matthew-Russo-311/Secure-Password-Manager.git
    cd Secure-Password-Manager

2. Create and activate a virtual environment:
bash
    python -m venv venv
    venv\Scripts\activate  # Windows
    source venv/bin/activate  # Mac/Linux

3. Install dependencies:
bash
    pip install -r requirements.txt

4. Create a `.env` file in the project root:
    SECRET_KEY=your_secret_key
    JWT_SECRET_KEY=your_jwt_secret_key
    DATABASE_URL=postgresql://postgres:yourpassword@localhost/password_manager
    ENCRYPTION_KEY=your_fernet_key

5. Create the database and run migrations:
bash
    psql -U postgres -c "CREATE DATABASE password_manager;"
    flask db upgrade

6. Run the app:
bash
    python run.py

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register a new user | No |
| POST | `/auth/login` | Login and receive JWT token | No |

### Password Entries

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/passwords/` | Create a new password entry | Yes |
| GET | `/passwords/` | Get all entries (paginated) | Yes |
| GET | `/passwords/<id>` | Get a single entry | Yes |
| PUT | `/passwords/<id>` | Update an entry | Yes |
| DELETE | `/passwords/<id>` | Delete an entry | Yes |

## Request & Response Examples

### Register
**POST** `/auth/register`
json
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123"
}

Response `201`:
json
{
    "message": "User registered successfully"
}

### Login
**POST** `/auth/login`
json
{
    "email": "john@example.com",
    "password": "securepassword123"
}

Response `200`:
json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

### Create Password Entry
**POST** `/passwords/`
Headers: `Authorization: Bearer <token>`
json
{
    "site_name": "GitHub",
    "site_username": "johndoe",
    "password": "mysecretpassword"
}

Response `201`:
json
{
    "message": "Password entry created successfully",
    "id": 1
}

### Get All Passwords (Paginated)
**GET** `/passwords/?page=1&per_page=10`
Headers: `Authorization: Bearer <token>`

Response `200`:
json
{
    "entries": [
        {
            "id": 1,
            "site_name": "GitHub",
            "site_username": "johndoe",
            "password": "mysecretpassword",
            "created_at": "2026-02-27T11:00:33.594187",
            "updated_at": "2026-02-27T11:00:33.594187"
        }
    ],
    "pagination": {
        "page": 1,
        "per_page": 10,
        "total": 1,
        "pages": 1,
        "has_next": false,
        "has_prev": false
    }
}

## Security

- Passwords are never stored in plain text — bcrypt hashing for user passwords, Fernet encryption for stored entries
- All password endpoints require a valid JWT token
- Users can only access their own entries
- Rate limiting on login endpoint (5 requests/minute) prevents brute force attacks
- Designed for deployment behind HTTPS

## Running Tests
bash
pytest app/tests/ -v

## Postman Collection

A Postman collection is included in the repository (`postman_collection.json`) with all endpoints pre-configured. Import it into Postman and set up an environment with `base_url` and `token` variables to get started immediately.

## Development Notes
Built as a learning project to develop skills in Flask, PostgreSQL, JWT authentication, and REST API design.