# AuthCore

AuthCore is a modular backend for basic authentication, build with FastAPI and designed for extensibility and clarity. It provides user management, authentication, and authorization features using modern Python standards.

## Features

- User registration, authentication, and management.
- JWT-based authentication.
- Password hashing with bcrypt.
- SQLite database integration.
- Hexagonal architecture for better separation of concerns.
- RESTful API design.
- Test coverage with pytest and pytest-cov.

## Project Structure

```
adapters/
  auth/                # JWT authentication service
  db/                  # SQLite user repository
  web/                 # FastAPI API, middlewares, routes, schemas
app/
  main.py              # Application entry point
config/
  settings.py          # Configuration management
core/
  entities/            # Domain models (User)
  ports/               # Repository interfaces
  use_cases/           # Business logic (CRUD, authentication)
  utils/               # Utility functions (password, query validation)
db/
  authcore.db          # SQLite database file
scripts/
  populate_db.py       # Script to populate the database
tests/
  unit/                # Unit tests for core features
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/AuthCore.git
cd AuthCore
```

2. Install dependencies:

```bash
poetry install
```

3. Set up the database:

```bash
make populate ARG=both
```

## Usage


1. Run the application:

```bash
make run
```

2. API Endpoints

You can access the API endpoints at `http://localhost:8000/docs` for the interactive Swagger UI.

3. Default User Credentials

In this app we have 3 user kinds:

- Admin: admin1@example.com / password
- User: user1@example.com / password
- Guest: guest1@example.com / password

The default password for all users is "123456".

## Testing and coverage

- Run all tests:

```bash
make test
```

- Run tests with coverage:

```bash
make test-coverage
```