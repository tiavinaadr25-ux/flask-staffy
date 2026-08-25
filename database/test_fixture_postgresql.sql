INSERT INTO managers (full_name, restaurant_name, email, password_hash)
VALUES (
    'Test Manager',
    'Test Bistro',
    'manager@staffly.com',
    '$2b$12$placeholder_hash_to_replace_in_real_fixture'
)
ON CONFLICT (email) DO NOTHING;

INSERT INTO employees (manager_id, full_name, role_title, email, phone, status)
SELECT
    managers.id,
    'Test Employee',
    'Server',
    'employee@staffly.com',
    '+33 6 00 00 00 00',
    'active'
FROM managers
WHERE managers.email = 'manager@staffly.com'
AND NOT EXISTS (
    SELECT 1
    FROM employees
    WHERE employees.email = 'employee@staffly.com'
);
