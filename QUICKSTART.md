# Bauliver Backend - Quick Start Guide

## Prerequisites

- Python 3.11+
- PostgreSQL database (or use SQLite for development)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/alcatrazarmy/bauliver-backend.git
cd bauliver-backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (optional):
```bash
cp .env.example .env
# Edit .env with your database credentials
```

## Running the Application

### Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- API: http://localhost:8000
- Interactive API docs (Swagger): http://localhost:8000/docs
- Alternative API docs (ReDoc): http://localhost:8000/redoc

### Running Tests

```bash
pytest tests/ -v
```

## API Endpoints

### Authentication

- **POST /api/auth/register** - Register a new user
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword",
    "name": "User Name",
    "role": "user"
  }
  ```

- **POST /api/auth/login** - Login and get JWT token
  - Form data: `username` (email), `password`
  - Returns: `{"access_token": "...", "token_type": "bearer"}`

### Users

- **GET /api/users/me** - Get current user profile (requires authentication)

### Permits

All permit endpoints require authentication (JWT token in Authorization header).

- **POST /api/permits/** - Create a new permit
- **GET /api/permits/** - List permits (users see own, admins see all)
- **GET /api/permits/{id}** - Get specific permit
- **PUT /api/permits/{id}** - Update a permit
- **DELETE /api/permits/{id}** - Delete a permit

## Database Migrations

### Initialize Alembic (already done)
```bash
alembic init migrations
```

### Create a new migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback migration
```bash
alembic downgrade -1
```

## Usage Example

### 1. Register a user
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123",
    "name": "John Doe"
  }'
```

### 2. Login and get token
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -F "username=john@example.com" \
  -F "password=password123"
```

### 3. Create a permit (using the token)
```bash
curl -X POST http://localhost:8000/api/permits/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Jane Smith",
    "address": "123 Main St",
    "system_size_kw": 7.5,
    "status": "pending"
  }'
```

### 4. List permits
```bash
curl http://localhost:8000/api/permits/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Security Notes

⚠️ **Important for Production:**
1. Change the `SECRET_KEY` in `app/auth.py` to a secure random string
2. Use environment variables for sensitive configuration
3. Update CORS settings in `app/main.py` to only allow specific origins
4. Use HTTPS in production
5. Implement rate limiting
6. Review and update password requirements

## Project Structure

```
bauliver-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── auth.py              # Authentication utilities
│   ├── config.py            # Configuration
│   ├── database.py          # Database setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   └── routers/             # API route handlers
│       ├── auth.py          # Auth endpoints
│       ├── users.py         # User endpoints
│       └── permits.py       # Permit endpoints
├── migrations/              # Alembic migrations
├── tests/                   # Test suite
├── requirements.txt         # Python dependencies
└── alembic.ini             # Alembic configuration
```

## Features Implemented

✅ **Authentication System**
- JWT-based authentication
- User registration and login
- Password hashing with bcrypt
- Protected routes with role-based access

✅ **User Management**
- User model with email, password, role, and status
- Current user profile endpoint

✅ **Permit Management**
- Full CRUD operations for permits
- Role-based access control (users see own permits, admins see all)
- Permit model with customer info, address, system size, status

✅ **Database**
- SQLAlchemy ORM
- Alembic migrations
- Support for PostgreSQL

✅ **Testing**
- Comprehensive test suite
- 17 tests covering auth, users, and permits
- Test fixtures for easy testing

## Next Steps

- [ ] Add pagination to list endpoints
- [ ] Implement permit status workflow
- [ ] Add file upload for permit PDFs
- [ ] Integrate with OpenSolar API
- [ ] Add email notifications
- [ ] Implement audit logging
- [ ] Add API rate limiting
- [ ] Deploy to production
