# django
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve
# internal
from .. import views
from ..models import Board, Topic


class TopicPostsTests(TestCase):
    """Topic Posts View Tests"""
    def setUp(self):
        user_data = {
            'username': 'test_user',
            'password': 's3cret'
        }
        user = User.objects.create_user(**user_data)
        board_data = {
            'name': 'test board',
            'description': 'test board desc'
        }
        board = Board.objects.create(**board_data)
        topic_data = {
            'subject': 'test topic',
            'board': board,
            'starter': user
        }
        topic = Topic.objects.create(**topic_data)

        url = reverse('topic_posts', kwargs={'pk': board.pk, 'topic_pk': topic.pk})
        self.response = self.client.get(url)

    def test_topic_posts_view_success_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_topic_posts_view_not_found_status_code(self):
        url = reverse('topic_posts', kwargs={'pk': 66, 'topic_pk': 666})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_topic_posts_view_resolves(self):
        view = resolve('/boards/1/topics/1')
        self.assertEqual(view.func, views.topic_posts)
