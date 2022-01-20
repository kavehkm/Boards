# django
from django.test import TestCase
from django.urls import resolve, reverse
# internal
from .. import views
from ..models import Board


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
