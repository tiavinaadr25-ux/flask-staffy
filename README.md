# Staffly Flask MVP

Staffly is a Flask web application built to support RNCP Bloc 2 expectations
and to move toward CDA expectations: layered architecture, secure server-side
features, relational and NoSQL data access, automated tests, code quality, and
deployment preparation.

## Main features

- Manager login with password hashing
- Dashboard with task metrics
- Task CRUD
- SQLAlchemy relational models
- Layered application package (`staffly/`)
- PostgreSQL-ready configuration for localhost and Railway
- AI task suggestions inside the task page
- MongoDB-ready history for AI suggestions
- Tally-ready demo request button on the landing page
- Docker and Docker Compose support
- GitHub Actions CI pipeline

## Application structure

```txt
app.py                  Entry point for Flask, Gunicorn, and tests
staffly/__init__.py     App factory
staffly/config.py       Environment and application settings
staffly/extensions.py   Flask extensions
staffly/models.py       SQLAlchemy models
staffly/security.py     Auth, CSRF, route protection
staffly/repositories.py SQL access layer
staffly/services.py     Business logic and MongoDB / AI services
staffly/routes.py       HTTP routes and template rendering
tests/                  Automated tests
docs/cda/               CDA-oriented technical documentation
```

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

## Docker setup

To start the application with PostgreSQL and MongoDB in containers:

```bash
docker compose up --build
```

The web application is then available at `http://localhost:8000`.

To stop the stack:

```bash
docker compose down
```

## Optional AI and NoSQL setup

- `MONGO_URI` enables MongoDB history for AI suggestions
- `MONGO_DB_NAME` selects the MongoDB database name
- `MONGO_COLLECTION_NAME` selects the MongoDB collection name
- `HUGGING_FACE_API_TOKEN` enables real AI calls
- `HUGGING_FACE_MODEL_URL` points to your Hugging Face inference endpoint
- `TALLY_DEMO_URL` links the landing page button to your Tally form

By default, the project uses the Hugging Face serverless inference pattern with
`https://api-inference.huggingface.co/models/<MODEL_ID>`.
The provided `.env.example` uses a small instruct model suited for demo flows.

Without these variables, the task suggestion feature still works in local fallback mode.

Demo account:

- Email: `manager@staffly.com`
- Password: `Staffly123!`

## Quality checks

```bash
black app.py tests
flake8 app.py tests
pytest
```

You can also use the provided `Makefile`:

```bash
make format
make lint
make test
```

## Continuous integration

The project includes a GitHub Actions workflow in:

```txt
.github/workflows/ci.yml
```

The pipeline runs:

- Black
- Flake8
- Pytest

The CI job starts a PostgreSQL service so the test suite can run in a setup
closer to production.

## CDA-oriented documentation

Additional technical documentation is available in:

- `docs/cda/architecture-couches.md`
- `docs/cda/plan-tests-cda.md`
- `docs/cda/devops-cda.md`
- `docs/cda/sequence-diagrams.md`
