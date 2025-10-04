# Django Universe - Ui File Management System

A professional file management system with user authentication, built with Django, Docker, and PostgreSQL.

## Features

- User authentication with JWT
- File upload and management
- SVG to PNG conversion
- Cloudinary integration for media storage
- RESTful API endpoints
- Dockerized development and production setup

## Prerequisites

- Docker Desktop
- Docker Compose
- Python 3.9+
- Cloudinary account (for media storage)

## Setup

1. Clone the repository:
```bash
git clone https://github.com/BodruddozaRedoy/Verslib-Mosabbir-Backend.git
cd django-universe
```
2. Create .env file:
```bash
cp .env.example .env
 ```

3. Update .env with your credentials:
```text
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DJANGO_SECRET_KEY=your-django-secret-key
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
 ```

## Running with Docker
```bash
docker-compose up --build
 ```

## API Endpoints
### Authentication
- POST /api/auth/register/ - User registration
- POST /api/auth/login/ - User login
- POST /api/auth/token/refresh/ - Refresh JWT token
### Files
- GET /api/files/ - List all files with categories filter
- GET /api/files/pk/ - Get file details
- GET /api/files/pk/copy/ - Get files svg code
### Categories
- GET /api/categories/ - List all categories

## Project Structure
```plaintext
django-universe/
├── core/                  # Django project
│   ├── settings.py        # Project settings
│   ├── urls.py            # Main URLs
│   └── wsgi.py            # WSGI config
├── Accounts/              # User authentication app
├── Files/                 # File management app
├── deploy/                # Deployment configs
│   └── nginx/             # Nginx config
├── docker-compose.yml     # Development Docker config
├── Dockerfile             # Docker configuration
└── requirements.txt       # Python dependencies
 ```

## Contributing
1. Fork the project
2. Create your feature branch ( git checkout -b feature/AmazingFeature )
3. Commit your changes ( git commit -m 'Add some AmazingFeature' )
4. Push to the branch ( git push origin feature/AmazingFeature )
5. Open a Pull Request
## License
MIT
