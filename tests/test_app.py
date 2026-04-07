from __future__ import annotations

import re


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
    assert b"Manage restaurant teams with one secure web application." in response.data


def test_dashboard_requires_login(client) -> None:
    response = client.get("/dashboard", follow_redirects=False)

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
