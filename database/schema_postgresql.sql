CREATE TABLE IF NOT EXISTS managers (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    restaurant_name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_managers_email ON managers (email);

CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    manager_id INTEGER NOT NULL REFERENCES managers(id) ON DELETE CASCADE,
    full_name VARCHAR(120) NOT NULL,
    role_title VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL DEFAULT '',
    phone VARCHAR(40) NOT NULL DEFAULT '',
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    manager_id INTEGER NOT NULL REFERENCES managers(id) ON DELETE CASCADE,
    employee_id INTEGER REFERENCES employees(id) ON DELETE SET NULL,
    title VARCHAR(140) NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    status VARCHAR(40) NOT NULL DEFAULT 'todo',
    due_date DATE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS leave_requests (
    id SERIAL PRIMARY KEY,
    manager_id INTEGER NOT NULL REFERENCES managers(id) ON DELETE CASCADE,
    employee_id INTEGER NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    reason TEXT NOT NULL DEFAULT '',
    status VARCHAR(40) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
