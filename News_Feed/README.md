# News Feed System

A Django-based news feed application with PostgreSQL database, running in Docker.

## Quick Start

### Prerequisites

- Docker & Docker Compose installed

### Setup

1. **Clone the repository**

```bash
git clone <repo-url>
cd News_Feed
```

2. **Create `.env` file**

```bash
cp .env.example .env
# Edit .env with your settings (optional - defaults are provided)
```

3. **Start the application**

```bash
docker-compose up --build
```

4. **Access the application**

- Main app: `http://localhost:8000`
- Admin panel: `http://localhost:8000/admin`

## Environment Variables

See `.env.example` for available configuration options.

### Default Credentials (for local development)

- Database user: `postgres`
- Database password: `1234`
- Django admin: Create via migrations or use `docker-compose exec web python manage.py createsuperuser`

## Services

- **web**: Django application (port 8000)
- **db**: PostgreSQL database (port 5432)

## Useful Commands

```bash
# View logs
docker-compose logs -f web

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Stop containers
docker-compose down
```

## Project Structure

- `News_Feed/`: Django project settings
- `pages/`: Main application
- `static/`: Static files (CSS, JS)
- `media/`: User-uploaded files
- `templates/`: HTML templates
