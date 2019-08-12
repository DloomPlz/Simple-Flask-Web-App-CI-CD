# tests/test_3_login_route.py

def test_login_empty_password(client):
    # testing errors
    rv = client.post("/api/v1/login", json={
        'username': 'testuser', 'password': ''
    })
    assert rv.status_code == 422

def test_login_empty_username(client):
    rv = client.post("/api/v1/login", json={
        'username': '', 'password': 'test_user'
    })
    assert rv.status_code == 422

def test_login_correct(client, global_data):
    rv = client.post("/api/v1/login", json={
        'username': 'testuser', 'password': 'test_user'
    })
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert "token" in json_data
    global_data['token'] = json_data['token']

def test_login_admin(client, global_data):
    rv = client.post("/api/v1/login", json={
        'username': 'testadmin', 'password': 'testadmin'
    })
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert "token" in json_data
    global_data['token_admin'] = json_data['token']

def test_login_wrong_username(client):
    rv = client.post("/api/v1/login", json={
        'username': 'testusernot', 'password': 'test_user'
    })
    assert rv.status_code == 404

def test_login_wrong_password(client):
    rv = client.post("/api/v1/login", json={
        'username': 'testuser', 'password': 'test_user_wrong'
    })
    assert rv.status_code == 401