from django.test import Client


def test_products_list_anonymous_user_status_code(client: Client):
    response = client.get("/products")
    assert response.status_code == 301


# def test_products_list_logged_user_status_code(client: Client):
#     client.force_login(user='testuser')
#     response = client.get("/products")
#     assert response.status_code == 200
