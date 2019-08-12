# tests/test_7_roles.py

def test_create_role_empty_name(client, global_data):
    rv = client.post('/api/v1/roles',
        headers={'Authorization': global_data['token_admin']},
        json={
        'name': '', 'description': 'test_role'
    })
    assert rv.status_code == 422


def test_create_role_empty_description(client, global_data):
    rv = client.post('/api/v1/roles',
        headers={'Authorization': global_data['token_admin']},
        json={
        'name': 'test_role', 'description': ''
    })
    assert rv.status_code == 422


def test_create_role_correct(client, global_data):
    rv = client.post('/api/v1/roles',
        headers={'Authorization': global_data['token_admin']},
        json={
        'name': 'test_role', 'description': 'test_role'
    })
    assert rv.status_code == 200


def test_create_role_conflict(client, global_data):
    rv = client.post('/api/v1/roles',
        headers={'Authorization': global_data['token_admin']},
        json={
        'name': 'test_role', 'description': 'test_role'
    })
    assert rv.status_code == 409


def test_delete_role_ok(client, global_data):
    rv = client.delete('/api/v1/roles/test_role',
        headers={'Authorization': global_data['token_admin']},
    )
    assert rv.status_code == 200


def test_delete_role_not_found(client, global_data):
    rv = client.delete('/api/v1/roles/test_role',
        headers={'Authorization': global_data['token_admin']},
    )
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert "err" in json_data


def test_reset_role(client, global_data):
    rv = client.post('/api/v1/roles',
        headers={'Authorization': global_data['token_admin']},
        json={
        'name': 'test_role', 'description': 'test_role'
    })


def test_add_role_to_user_not_found(client, global_data):
    rv = client.post('/api/v1/users/testuser404/roles/test_role',
        headers={'Authorization': global_data['token_admin']},
    )
    assert rv.status_code == 404


def test_add_role_to_user_role_not_found(client, global_data):
    rv = client.post('/api/v1/users/testuser/roles/test_role404',
        headers={'Authorization': global_data['token_admin']},
    )
    assert rv.status_code == 404


def test_add_role_to_user_ok(client, global_data):
    rv = client.post('/api/v1/users/testuser/roles/test_role',
        headers={'Authorization': global_data['token_admin']},
    )
    assert rv.status_code == 200


def test_remove_role_to_user_not_found(client, global_data):
    rv = client.delete('/api/v1/users/testuser404/roles/test_role',
        headers={'Authorization': global_data['token_admin']},
    )
    assert rv.status_code == 404


def test_remove_role_to_user_role_not_found(client, global_data):
    rv = client.delete('/api/v1/users/testuser/roles/test_role404',
        headers={'Authorization': global_data['token_admin']},
    )
    assert rv.status_code == 404


def test_remove_role_to_user_ok(client, global_data):
    rv = client.delete('/api/v1/users/testuser/roles/test_role',
        headers={'Authorization': global_data['token_admin']},
    )
    assert rv.status_code == 200