from django.test import Client


def test_my_restaurant_view_status_code(client: Client):
    response = client.get("/restaurant/")
    assert response.status_code == 302
