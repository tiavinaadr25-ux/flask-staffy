# Staffly Flask MVP

Staffly is a Flask web application built to support RNCP Bloc 2 expectations:
secure server-side features, a relational database, SQL access layers, testing,
code quality, and deployment preparation.

## Main features

- Manager login with password hashing
- Dashboard with task metrics
- Task CRUD
- SQLAlchemy relational models
- PostgreSQL-ready configuration for localhost and Railway
- AI task suggestions inside the task page
- MongoDB-ready history for AI suggestions
- Tally-ready demo request button on the landing page

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
