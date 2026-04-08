from __future__ import annotations

import re

from sqlalchemy import select

from app import Manager, db


def extract_csrf_token(html: str) -> str:
    match = re.search(r'name="csrf_token" value="([^"]+)"', html)
    assert match is not None
    return match.group(1)


def login_manager(client) -> None:
    response = client.get("/login")
    csrf_token = extract_csrf_token(response.data.decode("utf-8"))

    client.post(
        "/login",
        data={
            "csrf_token": csrf_token,
            "email": "manager@staffly.com",
            "password": "Staffly123!",
        },
        follow_redirects=True,
    )


def test_home_page_loads(client) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert b"G\xc3\xa9rez votre \xc3\xa9quipe" in response.data


def test_dashboard_requires_login(client) -> None:
    response = client.get("/dashboard", follow_redirects=False)

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_ai_suggestions_requires_login(client) -> None:
    response = client.get("/ai-suggestions", follow_redirects=False)

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_login_succeeds(client) -> None:
    response = client.get("/login")
    csrf_token = extract_csrf_token(response.data.decode("utf-8"))

    login_response = client.post(
        "/login",
        data={
            "csrf_token": csrf_token,
            "email": "manager@staffly.com",
            "password": "Staffly123!",
        },
        follow_redirects=True,
    )

    assert login_response.status_code == 200
    assert b"Welcome back." in login_response.data
    assert b"Test Manager" in login_response.data


def test_register_creates_account_and_redirects_dashboard(client, app) -> None:
    response = client.get("/register")
    csrf_token = extract_csrf_token(response.data.decode("utf-8"))

    register_response = client.post(
        "/register",
        data={
            "csrf_token": csrf_token,
            "full_name": "New Manager",
            "restaurant_name": "New Bistro",
            "email": "new.manager@staffly.com",
            "password": "Staffly456!",
            "password_confirmation": "Staffly456!",
        },
        follow_redirects=True,
    )

    assert register_response.status_code == 200
    assert b"Your Staffly account is ready." in register_response.data
    assert b"New Manager" in register_response.data
    assert b"Votre espace Staffly est pr\xc3\xaat" in register_response.data

    with app.app_context():
        manager = db.session.scalar(
            select(Manager).where(Manager.email == "new.manager@staffly.com")
        )
        assert manager is not None


def test_register_rejects_duplicate_email(client) -> None:
    response = client.get("/register")
    csrf_token = extract_csrf_token(response.data.decode("utf-8"))

    register_response = client.post(
        "/register",
        data={
            "csrf_token": csrf_token,
            "full_name": "Duplicate Manager",
            "restaurant_name": "Duplicate Bistro",
            "email": "manager@staffly.com",
            "password": "Staffly456!",
            "password_confirmation": "Staffly456!",
        },
    )

    assert register_response.status_code == 409
    assert b"An account already exists with this email." in register_response.data


def test_employee_can_be_created(client) -> None:
    login_manager(client)

    form_page = client.get("/employees/new")
    csrf_token = extract_csrf_token(form_page.data.decode("utf-8"))

    response = client.post(
        "/employees/new",
        data={
            "csrf_token": csrf_token,
            "full_name": "New Employee",
            "role_title": "Runner",
            "email": "new.employee@staffly.com",
            "phone": "+33 6 22 22 22 22",
            "status": "active",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Employee created successfully." in response.data
    assert b"New Employee" in response.data


def test_task_can_be_created(client) -> None:
    login_manager(client)

    form_page = client.get("/tasks/new")
    csrf_token = extract_csrf_token(form_page.data.decode("utf-8"))

    response = client.post(
        "/tasks/new",
        data={
            "csrf_token": csrf_token,
            "title": "Open the terrace area",
            "description": "Prepare the terrace before service.",
            "employee_id": "1",
            "status": "todo",
            "due_date": "2026-04-16",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Task created successfully." in response.data
    assert b"Open the terrace area" in response.data


def test_leave_request_can_be_created(client) -> None:
    login_manager(client)

    form_page = client.get("/leave-requests/new")
    csrf_token = extract_csrf_token(form_page.data.decode("utf-8"))

    response = client.post(
        "/leave-requests/new",
        data={
            "csrf_token": csrf_token,
            "employee_id": "1",
            "start_date": "2026-04-15",
            "end_date": "2026-04-16",
            "reason": "Personal reason",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Leave request created successfully." in response.data
    assert b"Personal reason" in response.data


def test_ai_suggestions_can_be_generated_in_fallback_mode(client) -> None:
    login_manager(client)

    page = client.get("/ai-suggestions")
    csrf_token = extract_csrf_token(page.data.decode("utf-8"))

    response = client.post(
        "/ai-suggestions",
        data={
            "csrf_token": csrf_token,
            "prompt": "service du midi avec terrasse",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"AI suggestions generated." in response.data
    assert b"service du midi avec terrasse" in response.data
    assert b"fallback" in response.data
