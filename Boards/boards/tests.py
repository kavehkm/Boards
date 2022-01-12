# django
from django.test import TestCase
from django.urls import resolve, reverse
# internal
from . import views


class HomeTests(TestCase):
    """Home View Tests"""
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_resolve_url(self):
        view = resolve('/')
        self.assertEqual(view.func, views.home)
