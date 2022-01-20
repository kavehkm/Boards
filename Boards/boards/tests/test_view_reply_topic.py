# django
from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
# internal
from .. import views
from ..models import Board, Topic


class ReplyTopicTests(TestCase):
    """Reply Topic View Tests"""
    def setUp(self):
        user_data = {
            'username': 'test_user',
            'password': 's3cret'
        }
        user = User.objects.create_user(**user_data)
        board_data = {
            'name': 'test board',
            'description': 'test description'
        }
        self.board = Board.objects.create(**board_data)
        topic_data = {
            'subject': 'test topic',
            'board': self.board,
            'starter': user,
        }
        self.topic = Topic.objects.create(**topic_data)

        self.client.login(**user_data)

    def test_reply_topic_view_success_status_code(self):
        url = reverse('reply_topic', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_reply_topic_view_not_found_status_code(self):
        url = reverse('reply_topic', kwargs={'pk': 66, 'topic_pk': 666})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_reply_topic_url_resolves(self):
        view = resolve('/boards/1/topics/1/reply')
        self.assertEqual(view.func, views.reply_topic)

    def test_reply_topic_view_unauthorized_request(self):
        self.client.logout()
        url = reverse('reply_topic', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})
        response = self.client.get(url)
        login_url = reverse('signin')
        self.assertRedirects(response, '{}?next={}'.format(login_url, url))
