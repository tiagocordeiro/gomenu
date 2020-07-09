from django.contrib.auth.models import User, Group
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse


class RestaurantViewsTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.client = Client()

        # Restaurant Manager User
        self.restaurant_manager = User.objects.create_user(username='jacob',
                                                           email='jacob@…',
                                                           password='top_secret')
        self.group = Group.objects.create(name='Restaurant Manager')
        self.group.user_set.add(self.restaurant_manager)

    def test_list_products_view_status_code_with_anonymous_user(self):
        self.client.logout()
        response = self.client.get(reverse('products_list'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/products/',
                             status_code=302, target_status_code=200)

    def test_list_products_view_status_code_with_logged_user(self):
        self.client.force_login(self.restaurant_manager)
        response = self.client.get(reverse('products_list'))

        self.assertEqual(response.status_code, 200)
