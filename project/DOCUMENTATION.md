# Job Portal - Authentication Module Documentation

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Features](#features)
4. [Project Structure](#project-structure)
5. [Technology Stack](#technology-stack)
6. [Setup & Installation](#setup--installation)
7. [Configuration](#configuration)
8. [API Documentation](#api-documentation)
9. [Security Features](#security-features)
10. [Database Schema](#database-schema)
11. [Frontend Components](#frontend-components)
12. [Development Guidelines](#development-guidelines)
13. [Running the Application](#running-the-application)

---

## Overview

This is a **Job Portal Authentication Module** built with FastAPI. It provides a complete user authentication system with role-based access control (RBAC) for a job listing platform. The module supports two user roles: **Job Seeker** and **Employer**.

The application features:
- User registration and login
- JWT-based authentication
- HTTP-only cookie security
- Role-based access control
- Modern, responsive web UI
- RESTful API endpoints
- Async database operations with PostgreSQL

---

## Architecture

### High-Level Architecture

```
┌─────────────────┐
│   Web Browser   │
│  (HTML/CSS/JS)  │
└────────┬────────┘
         │ HTTP Requests
         ▼
┌─────────────────┐
│   FastAPI App   │
│   (main.py)     │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────────┐
│ Routes │ │  Templates   │
│(auth)  │ │  (Jinja2)    │
└───┬────┘ └──────────────┘
    │
    ▼
┌─────────────────┐
│  Auth Module    │
│  (auth.py)      │
│  - JWT          │
│  - Password     │
│  - RBAC         │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────────┐
│ Models │ │  Database    │
│(ORM)   │ │ (PostgreSQL) │
└────────┘ └──────────────┘
```

### Request Flow

1. **UI Routes**: User accesses `/login`, `/register`, or `/dashboard`
2. **API Routes**: Frontend JavaScript makes AJAX calls to `/auth/*` endpoints
3. **Authentication**: `auth.py` handles JWT creation/verification and password hashing
4. **Database**: SQLAlchemy ORM interacts with PostgreSQL asynchronously
5. **Response**: HTML templates rendered with Jinja2 or JSON responses

---

## Features

### Authentication Features
- ✅ User registration with email and password
- ✅ User login with credential verification
- ✅ JWT token generation and validation
- ✅ HTTP-only cookie storage for enhanced security
- ✅ Token expiration (configurable, default: 60 minutes)
- ✅ Password hashing using bcrypt with SHA-256 pre-hashing
- ✅ Role-based access control (Job Seeker / Employer)
- ✅ User session management
- ✅ Protected routes with authentication middleware

### User Interface Features
- ✅ Modern, responsive design with dark theme
- ✅ Login page with form validation
- ✅ Registration page with role selection
- ✅ Protected dashboard with user information
- ✅ Role-specific content display
- ✅ Error handling and user feedback
- ✅ Automatic redirects for unauthenticated users

### API Features
- ✅ RESTful API design
- ✅ JSON request/response format
- ✅ Bearer token authentication support
- ✅ Cookie-based authentication for web UI
- ✅ Comprehensive error handling
- ✅ Input validation with Pydantic schemas

---

## Project Structure

```
project/
├── __init__.py                 # Package initialization
├── main.py                     # FastAPI application entry point
├── database.py                 # Database connection and session management
├── models.py                   # SQLAlchemy ORM models
├── schemas.py                  # Pydantic validation schemas
├── auth.py                     # Authentication utilities (JWT, password hashing, RBAC)
├── requirements.txt            # Python dependencies
├── README.md                   # Quick start guide
├── DOCUMENTATION.md            # This comprehensive documentation
│
├── routes/
│   ├── __init__.py
│   └── auth_routes.py         # Authentication API and UI routes
│
├── templates/                 # Jinja2 HTML templates
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   └── dashboard.html         # Protected dashboard
│
└── static/                    # Static assets
    ├── style.css              # Application stylesheet
    └── auth.js                # Frontend JavaScript for auth flows
```

### File Descriptions

#### Core Application Files

**`main.py`**
- FastAPI application initialization
- Lifespan context manager for database table creation
- Static file mounting
- Route registration
- Root endpoint redirect

**`database.py`**
- Async SQLAlchemy engine configuration
- Database URL management (environment variable with fallback)
- Async session factory
- FastAPI dependency for database sessions

**`models.py`**
- SQLAlchemy declarative base
- `User` model with fields:
  - `id`: Primary key
  - `email`: Unique, indexed
  - `hashed_password`: Bcrypt hash
  - `role`: "job_seeker" or "employer"
  - `is_active`: Account status flag
  - `created_at`: Timestamp with timezone

**`schemas.py`**
- Pydantic models for request/response validation:
  - `UserCreate`: Registration payload
  - `UserLogin`: Login payload
  - `UserPublic`: User data response (excludes password)
  - `TokenResponse`: JWT token response

**`auth.py`**
- Password hashing (bcrypt + SHA-256 pre-hash)
- JWT token creation and validation
- Cookie management (set/clear)
- FastAPI dependencies:
  - `get_current_user`: Required authentication
  - `get_current_user_optional`: Optional authentication (for UI)
  - `require_role`: Role-based access control factory

**`routes/auth_routes.py`**
- API endpoints:
  - `POST /auth/register`: User registration
  - `POST /auth/login`: User login
  - `GET /auth/me`: Get current user
  - `POST /auth/logout`: Logout
- UI routes:
  - `GET /register`: Registration page
  - `GET /login`: Login page
  - `GET /dashboard`: Protected dashboard
  - `GET /logout`: Logout and redirect

#### Frontend Files

**`templates/login.html`**
- Login form with email and password fields
- Error message display
- Link to registration page

**`templates/register.html`**
- Registration form with email, password, and role selection
- Success/error message display
- Link to login page

**`templates/dashboard.html`**
- User information display
- Role-specific content sections
- Logout button

**`static/auth.js`**
- Form submission handlers
- API communication (fetch)
- Error parsing and display
- Redirect logic

**`static/style.css`**
- Modern dark theme styling
- Responsive design
- Card-based layout
- Form styling
- Alert components

---

## Technology Stack

### Backend
- **FastAPI 0.115.6**: Modern, fast web framework for building APIs
- **Uvicorn 0.32.1**: ASGI server for running FastAPI
- **SQLAlchemy 2.0.36**: Async ORM for database operations
- **asyncpg 0.30.0**: Async PostgreSQL driver
- **Passlib 1.7.4**: Password hashing library (bcrypt)
- **python-jose 3.3.0**: JWT token creation and validation
- **Pydantic**: Data validation (included with FastAPI)
- **Jinja2 3.1.4**: Template engine for HTML rendering

### Database
- **PostgreSQL**: Relational database (version 12+ recommended)

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS variables
- **Vanilla JavaScript**: No framework dependencies

---

## Setup & Installation

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

### Step 1: Clone/Download the Project
Ensure you have the project files in your workspace.

### Step 2: Create Virtual Environment

**Windows PowerShell:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up PostgreSQL Database
1. Create a PostgreSQL database:
```sql
CREATE DATABASE job_portal;
```

2. Ensure PostgreSQL is running and accessible.

### Step 5: Configure Environment Variables

**Windows PowerShell:**
```powershell
$env:DATABASE_URL="postgresql+asyncpg://postgres:your_password@localhost:5432/job_portal"
$env:SECRET_KEY="your-secret-key-change-in-production"
$env:ACCESS_TOKEN_EXPIRE_MINUTES="60"
$env:COOKIE_SECURE="false"
```

**Linux/macOS:**
```bash
export DATABASE_URL="postgresql+asyncpg://postgres:your_password@localhost:5432/job_portal"
export SECRET_KEY="your-secret-key-change-in-production"
export ACCESS_TOKEN_EXPIRE_MINUTES="60"
export COOKIE_SECURE="false"
```

**Note**: The application has a fallback database URL in `database.py` for local development, but it's recommended to set environment variables.

### Step 6: Run the Application

**Option 1: Using Uvicorn (Recommended)**
```bash
uvicorn project.main:app --reload
```

**Option 2: Direct Python Execution**
```bash
python main.py
```

The application will be available at: `http://127.0.0.1:8000`

---

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://postgres:bavaguru12@localhost:5432/job_portal` | No (has fallback) |
| `SECRET_KEY` | JWT signing secret | `"dev-only-change-me"` | **Yes (in production)** |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT expiration time | `60` | No |
| `COOKIE_SECURE` | Enable secure cookies (HTTPS) | `"false"` | No |

### Database URL Format
```
postgresql+asyncpg://username:password@host:port/database_name
```

**Special Characters in Password:**
- URL-encode special characters (e.g., `@` becomes `%40`)
- Example: `password@123` → `password%40123`

### Security Recommendations

1. **Production Environment:**
   - Set `SECRET_KEY` to a strong, random string
   - Set `COOKIE_SECURE="true"` when using HTTPS
   - Use environment-specific database credentials
   - Never commit secrets to version control

2. **Token Expiration:**
   - Adjust `ACCESS_TOKEN_EXPIRE_MINUTES` based on security requirements
   - Consider implementing refresh tokens for longer sessions

---

## API Documentation

### Base URL
```
http://127.0.0.1:8000
```

### Authentication

The API supports two authentication methods:

1. **HTTP-only Cookie** (for web UI)
   - Automatically set on login
   - Sent with every request automatically

2. **Bearer Token** (for API clients)
   - Header: `Authorization: Bearer <token>`
   - Token obtained from `/auth/login` response

### Endpoints

#### 1. Register User

**Endpoint:** `POST /auth/register`

**Description:** Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "role": "job_seeker"
}
```

**Request Schema:**
- `email`: Valid email address (EmailStr)
- `password`: String, 8-128 characters
- `role`: Either `"job_seeker"` or `"employer"`

**Response:** `201 Created`
```json
{
  "id": 1,
  "email": "user@example.com",
  "role": "job_seeker",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**
- `400 Bad Request`: Email already registered
- `422 Unprocessable Entity`: Validation error

---

#### 2. Login

**Endpoint:** `POST /auth/login`

**Description:** Authenticate user and receive JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Request Schema:**
- `email`: Valid email address
- `password`: String, 1-128 characters

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Note:** Token is also set as HTTP-only cookie named `access_token`.

**Error Responses:**
- `401 Unauthorized`: Invalid email or password
- `403 Forbidden`: User account is inactive
- `422 Unprocessable Entity`: Validation error

---

#### 3. Get Current User

**Endpoint:** `GET /auth/me`

**Description:** Retrieve authenticated user's information.

**Authentication:** Required (Cookie or Bearer token)

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "role": "job_seeker",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**
- `401 Unauthorized`: Not authenticated or invalid token
- `403 Forbidden`: User account is inactive

---

#### 4. Logout

**Endpoint:** `POST /auth/logout`

**Description:** Logout user (clears authentication cookie).

**Authentication:** Optional

**Response:** `200 OK`
```json
{
  "detail": "Logged out."
}
```

**Note:** This endpoint clears the HTTP-only cookie. For stateless JWTs, the token remains valid until expiration.

---

### UI Routes

#### 1. Registration Page
- **Endpoint:** `GET /register`
- **Description:** Renders registration form
- **Response:** HTML page

#### 2. Login Page
- **Endpoint:** `GET /login`
- **Description:** Renders login form
- **Response:** HTML page

#### 3. Dashboard
- **Endpoint:** `GET /dashboard`
- **Description:** Protected dashboard page
- **Authentication:** Required
- **Response:** HTML page (redirects to `/login` if not authenticated)

#### 4. Logout (UI)
- **Endpoint:** `GET /logout`
- **Description:** Logout and redirect to login
- **Response:** Redirect to `/login`

#### 5. Root
- **Endpoint:** `GET /`
- **Description:** Redirects to `/dashboard`
- **Response:** Redirect (302)

---

## Security Features

### Password Security

1. **Bcrypt Hashing**
   - Uses bcrypt algorithm for password hashing
   - Automatic salt generation
   - Configurable cost factor (default: 12 rounds)

2. **SHA-256 Pre-hashing**
   - Passwords are pre-hashed with SHA-256 before bcrypt
   - Prevents bcrypt's 72-byte limit issue
   - Ensures consistent handling of long passwords

3. **Password Requirements**
   - Minimum length: 8 characters
   - Maximum length: 128 characters
   - Validated on both frontend and backend

### JWT Security

1. **Token Structure**
   - Algorithm: HS256 (HMAC-SHA256)
   - Claims:
     - `sub`: User email (subject)
     - `role`: User role
     - `iat`: Issued at timestamp
     - `exp`: Expiration timestamp

2. **Token Storage**
   - HTTP-only cookies (web UI)
   - Prevents XSS attacks
   - SameSite=Lax protection against CSRF

3. **Token Validation**
   - Signature verification
   - Expiration checking
   - User existence validation
   - Active status checking

### Cookie Security

- **HttpOnly**: Prevents JavaScript access
- **Secure**: Enabled in production (HTTPS only)
- **SameSite**: Lax (CSRF protection)
- **Path**: `/` (application-wide)
- **Max-Age**: Matches token expiration

### Role-Based Access Control (RBAC)

- Two roles: `job_seeker` and `employer`
- Role validation on protected endpoints
- Role-specific UI content
- Extensible for future role-based features

### Input Validation

- **Pydantic Schemas**: Request/response validation
- **Email Validation**: Built-in email format checking
- **SQL Injection Protection**: SQLAlchemy parameterized queries
- **XSS Protection**: Jinja2 auto-escaping

---

## Database Schema

### Users Table

**Table Name:** `users`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, INDEX | Auto-incrementing user ID |
| `email` | VARCHAR(320) | UNIQUE, INDEX, NOT NULL | User email address |
| `hashed_password` | VARCHAR(255) | NOT NULL | Bcrypt password hash |
| `role` | VARCHAR(32) | NOT NULL | User role: "job_seeker" or "employer" |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT TRUE | Account active status |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Account creation timestamp |

### Indexes
- Primary key index on `id`
- Unique index on `email`
- Index on `email` for faster lookups

### Relationships
Currently, the `users` table is standalone. Future modules may add:
- Job listings (for employers)
- Job applications (for job seekers)
- User profiles
- etc.

---

## Frontend Components

### JavaScript (`static/auth.js`)

**Functions:**

1. **`show(el, message)`**
   - Displays an element with a message
   - Removes `hidden` class

2. **`hide(el)`**
   - Hides an element
   - Adds `hidden` class

3. **`parseError(res)`**
   - Parses error response from API
   - Handles JSON and text responses

4. **`registerFlow()`**
   - Handles registration form submission
   - Validates input
   - Makes POST request to `/auth/register`
   - Shows success/error messages
   - Redirects to login on success

5. **`loginFlow()`**
   - Handles login form submission
   - Validates input
   - Makes POST request to `/auth/login`
   - Sets authentication cookie
   - Redirects to dashboard on success

### CSS (`static/style.css`)

**Design System:**
- Dark theme with gradient background
- CSS custom properties (variables)
- Responsive design
- Card-based layout
- Modern form styling

**Key Components:**
- `.container`: Centered layout
- `.card`: Glass-morphism card design
- `.form`: Form layout
- `.btn`: Button styles (primary/secondary)
- `.alert`: Error/success messages
- `.kv`: Key-value display
- `.panel`: Content sections

---

## Development Guidelines

### Code Style

1. **Import Organization**
   - Standard library imports first
   - Third-party imports second
   - Local imports last
   - Supports both package and script-style imports

2. **Type Hints**
   - Use type hints for function parameters and returns
   - Use `Annotated` for FastAPI dependencies

3. **Async/Await**
   - All database operations are async
   - Use `async`/`await` consistently

4. **Error Handling**
   - Use FastAPI's `HTTPException` for API errors
   - Provide meaningful error messages
   - Handle database integrity errors

### Adding New Features

1. **New API Endpoint:**
   - Add route in `routes/auth_routes.py` or create new router
   - Define Pydantic schema in `schemas.py` if needed
   - Use `Depends(get_current_user)` for authentication
   - Use `Depends(require_role(...))` for role-based access

2. **New Database Model:**
   - Define model in `models.py`
   - Inherit from `Base`
   - Tables are auto-created on startup (use Alembic in production)

3. **New UI Page:**
   - Create HTML template in `templates/`
   - Add route in `routes/auth_routes.py`
   - Use Jinja2 templating
   - Link CSS/JS from `static/`

### Testing Recommendations

1. **Unit Tests:**
   - Test password hashing/verification
   - Test JWT creation/validation
   - Test role-based access control

2. **Integration Tests:**
   - Test API endpoints
   - Test authentication flows
   - Test database operations

3. **E2E Tests:**
   - Test complete user flows
   - Test UI interactions

### Production Considerations

1. **Database Migrations:**
   - Replace auto-table creation with Alembic migrations
   - Version control database schema changes

2. **Error Logging:**
   - Implement proper logging
   - Use structured logging (JSON)
   - Log security events

3. **Rate Limiting:**
   - Implement rate limiting on auth endpoints
   - Prevent brute force attacks

4. **CORS:**
   - Configure CORS if serving API separately
   - Restrict allowed origins

5. **HTTPS:**
   - Use HTTPS in production
   - Set `COOKIE_SECURE="true"`

6. **Monitoring:**
   - Add health check endpoints
   - Monitor database connections
   - Track authentication failures

---

## Running the Application

### Development Mode

```bash
uvicorn project.main:app --reload
```

**Features:**
- Auto-reload on code changes
- Debug mode enabled
- Detailed error messages

### Production Mode

```bash
uvicorn project.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Features:**
- Multiple worker processes
- Production-optimized settings
- No auto-reload

### Accessing the Application

1. **Web UI:**
   - Registration: `http://127.0.0.1:8000/register`
   - Login: `http://127.0.0.1:8000/login`
   - Dashboard: `http://127.0.0.1:8000/dashboard`

2. **API Documentation:**
   - Swagger UI: `http://127.0.0.1:8000/docs`
   - ReDoc: `http://127.0.0.1:8000/redoc`

3. **API Endpoints:**
   - Base URL: `http://127.0.0.1:8000`
   - Auth endpoints: `/auth/*`

---

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify PostgreSQL is running
   - Check `DATABASE_URL` format
   - Ensure database exists
   - Verify credentials

2. **Import Errors**
   - Ensure virtual environment is activated
   - Verify all dependencies are installed
   - Check Python path

3. **Port Already in Use**
   - Change port: `uvicorn project.main:app --port 8001`
   - Kill existing process on port 8000

4. **Cookie Not Set**
   - Check browser console for errors
   - Verify `credentials: "same-origin"` in fetch requests
   - Check CORS settings if using different origin

5. **Token Expired**
   - Default expiration: 60 minutes
   - Adjust `ACCESS_TOKEN_EXPIRE_MINUTES`
   - Re-login to get new token

---

## Future Enhancements

Potential features for future development:

1. **Password Reset**
   - Email-based password reset flow
   - Secure token generation
   - Password reset page

2. **Email Verification**
   - Send verification email on registration
   - Verify email before account activation

3. **Refresh Tokens**
   - Long-lived refresh tokens
   - Automatic token refresh

4. **Two-Factor Authentication (2FA)**
   - TOTP-based 2FA
   - SMS-based 2FA option

5. **Social Authentication**
   - OAuth integration (Google, GitHub, etc.)
   - Social login buttons

6. **User Profiles**
   - Extended user information
   - Profile management endpoints

7. **Session Management**
   - Active session tracking
   - Logout from all devices

---

## License

This documentation is provided as-is for the Job Portal Authentication Module.

---

## Contact & Support

For issues, questions, or contributions, please refer to the project repository or contact the development team.

---

**Documentation Version:** 1.0  
**Last Updated:** 2024  
**Application Version:** Based on FastAPI 0.115.6

