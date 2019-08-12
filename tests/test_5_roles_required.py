# tests/test_5_roles_required.py

def test_login_required_not_allowed(client, global_data):
    rv = client.get('/admin', headers={'Authorization': global_data['token']})
    assert rv.status_code == 401


def test_roles_required(client, global_data):
    rv = client.get('/admin', headers={'Authorization': global_data['token_admin']})
    assert rv.status_code == 200