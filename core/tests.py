from django.test import Client


def test_home_status_code(client: Client):
    response = client.get('/')
    assert response.status_code == 200


def test_dashboard_status_code(client: Client):
    response = client.get('/dashboard/')
    assert response.status_code == 200
