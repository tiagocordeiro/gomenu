from django.contrib.auth.models import User, Group
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from .admin import CompanyAdmin
from .facade import get_dashboard_data_summary
from .models import Company


# Create your tests here.
from .templatetags.core_extras import has_group


class IndexViewTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.client = Client()

        self.company = Company.objects.create(name='My Restaurant',
                                              address='FooBar street, 666',
                                              phone='(11) 1234-5678',
                                              website='https://www.mulhergorila.com',
                                              facebook='https://www.facebook.com',
                                              instagram='https://www.instagram.com')

        # Staff user
        self.staff_user = User.objects.create_user(username='jacob',
                                                   email='jacob@…',
                                                   password='top_secret')
        self.group = Group.objects.create(name='Staff Test')
        self.group.user_set.add(self.staff_user)

        # Super user
        self.super_user = User.objects.create_superuser(username='master',
                                                        email='master@…',
                                                        password='top_secret')

        # Customer user
        self.customer_user = User.objects.create_user(username='customer',
                                                      email='customer@…',
                                                      password='secret')
        self.customer_group = Group.objects.create(name="Customer")
        self.customer_group.user_set.add(self.customer_user)

    def test_index_page_status_code_is_ok_with_noon_logged_user(self):
        self.client.logout()
        request = self.client.get(reverse('index'))

        self.assertEqual(request.status_code, 200)

    def test_index_page_status_code_is_302_with_logged_user(self):
        self.client.force_login(self.staff_user)
        request = self.client.get(reverse('index'))

        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request,
                             '/dashboard/',
                             status_code=302,
                             target_status_code=200)

    def test_index_page_status_code_with_customer_logged_user(self):
        self.client.force_login(self.customer_user)
        request = self.client.get(reverse('index'))

        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request,
                             '/dashboard/',
                             status_code=302,
                             target_status_code=200)

    def test_dashboard_page_content_with_customer_logged_user(self):
        self.client.force_login(self.customer_user)
        request = self.client.get(reverse('dashboard'))

        self.assertEqual(request.status_code, 200)
        self.assertContains(request, 'Cupons')

    def test_company_name_return_str(self):
        company = Company.objects.get(name=self.company.name)
        self.assertEqual(company.__str__(), self.company.name)

    def test_company_admin_add_company_return_false(self):
        request = reverse('admin:core_company_changelist')
        has_add_permission = CompanyAdmin.has_add_permission(self.company,
                                                             request)
        self.assertEqual(has_add_permission, False)

    def test_returns_true_when_no_business_data_exists(self):
        self.company.delete()

        request = reverse('admin:core_company_changelist')
        has_add_permission = CompanyAdmin.has_add_permission(self.company,
                                                             request)
        self.assertEqual(has_add_permission, True)

    def test_dashboard_status_code_with_logged_user(self):
        self.client.force_login(self.staff_user)
        request = self.client.get(reverse('dashboard'))

        self.assertEqual(request.status_code, 200)
        self.assertContains(request, 'goMenu')

    def test_dashboard_status_code_with_no_logged_user(self):
        self.client.logout()
        request = self.client.get(reverse('dashboard'))

        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request,
                             '/accounts/login/?next=/dashboard/',
                             status_code=302,
                             target_status_code=200)

    def test_get_dashboardcontext_facade(self):
        context = get_dashboard_data_summary(self.super_user)
        self.assertIn('total_products', context)

    def test_has_group_filter_attribut_error(self):
        context = has_group('satringqq', 'Customer')
        self.assertEqual(False, context)
