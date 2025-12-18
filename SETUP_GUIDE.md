# Job Portal - Setup and Installation Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Database Setup](#database-setup)
   - [PostgreSQL Installation](#postgresql-installation)
   - [PgAdmin 4 Setup](#pgadmin-4-setup)
   - [Create Database](#create-database)
3. [Project Setup](#project-setup)
   - [Environment Setup](#environment-setup)
   - [Install Dependencies](#install-dependencies)
   - [Configuration](#configuration)
4. [Database Initialization](#database-initialization)
5. [Running the Application](#running-the-application)
6. [Accessing the Application](#accessing-the-application)
7. [Troubleshooting](#troubleshooting)
8. [Next Steps](#next-steps)

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 13 or higher
- PgAdmin 4
- Git (optional, for version control)
- Terminal/Command Prompt access
- Administrator/root privileges (for installation)

## Database Setup

### PostgreSQL Installation

#### Windows
1. Download the PostgreSQL installer from [postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
2. Run the installer and follow the wizard
   - Remember the password you set for the postgres user
   - Note the port number (default: 5432)
   - Keep the default components selected
3. Complete the installation

#### macOS
```bash
# Using Homebrew
brew install postgresql@14
brew services start postgresql@14
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### PgAdmin 4 Setup

#### Windows
- Installed automatically with PostgreSQL installer
- Launch from Start Menu

#### macOS
```bash
brew install --cask pgadmin4
```

#### Linux (Ubuntu/Debian)
```bash
curl -fsSL https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/pgadmin.gpg
sudo sh -c 'echo "deb https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list'
sudo apt update
sudo apt install pgadmin4
```

### Create Database

1. Open PgAdmin 4
2. Connect to your PostgreSQL server
   - Right-click on "Servers" > Create > Server
   - General tab:
     - Name: `JobPortal`
   - Connection tab:
     - Host name/address: `localhost`
     - Port: `5432`
     - Maintenance database: `postgres`
     - Username: `postgres`
     - Password: [your postgres password]
3. Create a new database:
   - Right-click on "Databases" > Create > Database
   - Name: `job_portal`
   - Owner: `postgres`

## Project Setup

### Environment Setup

1. Clone the repository (if applicable) or create a new directory:
   ```bash
   git clone [repository-url]
   cd job-portal
   ```
   OR
   ```bash
   mkdir job-portal
   cd job-portal
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

### Install Dependencies

1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
   
   If `requirements.txt` doesn't exist, install them manually:
   ```bash
   pip install fastapi uvicorn sqlalchemy asyncpg python-jose[cryptography] passlib[bcrypt] python-multipart python-dotenv jinja2 email-validator
   ```

### Configuration

1. Create a `.env` file in your project root with the following content:
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:yourpassword@localhost:5432/job_portal
   SECRET_KEY=your-secret-key-here-change-in-production
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   COOKIE_SECURE=false  # Set to true in production with HTTPS
   ```

2. Replace `yourpassword` with your PostgreSQL password and generate a strong `SECRET_KEY`.

## Database Initialization

1. Run the following command to create database tables:
   ```bash
   python -c "from database import init_db; import asyncio; asyncio.run(init_db())"
   ```

   Or run the application once (it will create tables on startup):
   ```bash
   uvicorn main:app --reload
   ```

## Running the Application

1. Start the development server:
   ```bash
   uvicorn main:app --reload
   ```

2. The application will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Accessing the Application

1. Open your web browser and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000)
2. You will be redirected to the login page
3. Click on "Register" to create a new account
4. After registration, log in with your credentials
5. You will be redirected to the dashboard upon successful login

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL service is running
- Verify database credentials in `.env` file
- Check if the database `job_portal` exists
- Make sure the user has proper permissions

### Port Conflicts
If port 8000 is in use, specify a different port:
```bash
uvicorn main:app --reload --port 8001
```

### Missing Dependencies
Ensure all required packages are installed:
```bash
pip install -r requirements.txt
```

### Common Errors
- **"Module not found" errors**: Activate your virtual environment
- **Database connection errors**: Check PostgreSQL service status and credentials
- **JWT errors**: Ensure `SECRET_KEY` is properly set in `.env`

## Next Steps

1. **Production Deployment**:
   - Set up a production server (e.g., Nginx + Gunicorn)
   - Configure HTTPS with Let's Encrypt
   - Set proper environment variables in production

2. **Security Enhancements**:
   - Implement rate limiting
   - Add CORS middleware
   - Set up proper logging
   - Enable CSRF protection

3. **Additional Features**:
   - Password reset functionality
   - Email verification
   - User profile management
   - Role-based access control enhancements

4. **Monitoring and Maintenance**:
   - Set up application monitoring
   - Regular database backups
   - Performance optimization

---

For support or to report issues, please contact [your-email@example.com] or open an issue in the project repository.
