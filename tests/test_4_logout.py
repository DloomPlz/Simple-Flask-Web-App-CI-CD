# tests/test_3_login_route.py

def test_login_before_logout(client, global_data):
    correct = client.post("/api/v1/login", json={
        'username': 'testuser', 'password': 'test_user'
    })
    json_data = correct.get_json()
    global_data['old_token'] = json_data['token']


def test_logout(client, global_data):
    rv = client.post('/api/v1/logout', headers={'Authorization': global_data['old_token']})
    assert rv.status_code == 200


def test_login_required_invalid_token(client, global_data):
    rv = client.get('/need_login', headers={'Authorization': global_data['old_token']})
    assert rv.status_code == 401
    del global_data["old_token"]