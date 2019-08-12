# tests/test_2_signup_route.py


def test_signup_empty_password(client):
    rv = client.post("/api/v1/signup", json={
        'username': 'testuser', 'password': '', 'email': 'test_user@mail.com'
    })
    assert rv.status_code == 422


def test_signup_empty_username(client):
    rv = client.post("/api/v1/signup", json={
        'username': '', 'password': 'test_user', 'email': 'test_user@mail.com'
    })
    assert rv.status_code == 422


def test_signup_empty_email(client):
    rv = client.post("/api/v1/signup", json={
        'username': 'testuser', 'password': 'test_user', 'email': ''
    })
    assert rv.status_code == 422

def test_signup_invalid_username(client):
    rv = client.post("/api/v1/signup", json={
        'username': '--test-user%/!~02--', 'password': 'test_user', 'email': 'test_user@mail.com'
    })
    assert rv.status_code == 422

def test_signup_correct(client):
    rv = client.post("/api/v1/signup", json={
        'username': 'testuser', 'password': 'test_user', 'email': 'test_user@mail.com'
    })
    assert rv.status_code == 200
    assert b'welcome' in rv.data

def test_root_endpoint(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'testuser' in rv.data


def test_signup_username_taken(client):
    rv = client.post("/api/v1/signup", json={
        'username': 'testuser', 'password': 'test_user', 'email': 'test_user@mail.com'
    })
    assert rv.status_code == 409


def test_signup_email_taken(client):
    rv = client.post("/api/v1/signup", json={
        'username': 'testuser', 'password': 'test_user', 'email': 'test_user@mail.com'
    })
    assert rv.status_code == 409