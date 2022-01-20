# django
from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
# internal
from .. import views
from ..models import Board


class NewTopicTests(TestCase):
    """New Topic View Tests"""
    def setUp(self):
        data = {
            'name': 'test board',
            'description': 'test description'
        }
        self.board = Board.objects.create(**data)
        user_data = {
            'username': 'test_user',
            'password': 's3cret'
        }
        User.objects.create_user(**user_data)
        self.client.login(**user_data)

    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic', kwargs={'pk': self.board.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 666})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_new_topic_url_resolves(self):
        view = resolve('/boards/1/new')
        self.assertEqual(view.func, views.new_topic)

    def test_new_topic_view_unauthorized_request(self):
        self.client.logout()
        url = reverse('new_topic', kwargs={'pk': self.board.pk})
        response = self.client.get(url)
        login_url = reverse('signin')
        self.assertRedirects(response, '{}?next={}'.format(login_url, url))
