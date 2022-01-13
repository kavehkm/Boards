# django
from django.test import TestCase
from django.urls import resolve, reverse
# internal
from . import views
from .models import Board


class HomeTests(TestCase):
    """Home View Tests"""
    def setUp(self):
        data = {
            'name': 'test board',
            'description': 'test description'
        }
        self.board = Board.objects.create(**data)
        self.response = self.client.get(reverse('home'))

    def test_home_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_home_view_resolve_url(self):
        view = resolve('/')
        self.assertEqual(view.func, views.home)

    def test_home_view_contains_link_topics_page(self):
        board_topic_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{}"'.format(board_topic_url))


class BoardTopicsTests(TestCase):
    """Board Topics View Tests"""
    def setUp(self):
        data = {
            'name': 'test board',
            'description': 'test description'
        }
        board = Board.objects.create(**data)
        url = reverse('board_topics', kwargs={'pk': board.pk})
        self.response = self.client.get(url)

    def test_board_topics_success_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 666})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_board_topics_url_resolves(self):
        view = resolve('/boards/1')
        self.assertEqual(view.func, views.board_topics)
