# tests/test_4_login_required.py

def test_login_required(client, global_data):
    rv = client.get('/need_login', headers={'Authorization': global_data['token']})
    assert rv.status_code == 200


def test_login_required_missing_token(client):
    rv = client.get('/need_login')
    assert rv.status_code == 400


def test_login_required_invalid_token(client):
    rv = client.get('/need_login', headers={'Authorization': "test.test.test"})
    assert rv.status_code == 401