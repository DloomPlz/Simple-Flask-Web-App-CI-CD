# tests/test_1_root.py

def test_root_endpoint(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Hello, World!' in rv.data