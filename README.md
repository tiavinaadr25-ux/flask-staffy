# Staffly Flask MVP

Staffly is a Flask web application built to support RNCP Bloc 2 expectations:
secure server-side features, a relational database, SQL access layers, testing,
code quality, and deployment preparation.

## Main features

- Manager login with password hashing
- Dashboard with staff, tasks, and leave request metrics
- Employee CRUD
- Task CRUD
- Leave request management
- SQLAlchemy relational models
- PostgreSQL-ready configuration for localhost and Railway

## Local setup

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements-dev.txt
   ```

3. Create the local PostgreSQL database if needed:

   ```bash
   psql -U postgres -f database/init_local_postgres.sql
   ```

4. Copy the environment file:

   ```bash
   cp .env.example .env
   ```

5. Initialize and seed the application:

   ```bash
   flask --app app init-db
   flask --app app seed-demo-data
   ```

6. Run the application:

   ```bash
   flask --app app run
   ```

Demo account:

- Email: `manager@staffly.com`
- Password: `Staffly123!`

## Quality checks

```bash
black app.py tests
flake8 app.py tests
pytest
```
