# django
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import Truncator


class Board(models.Model):
    """Board Model"""
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def absolute_url(self):
        return reverse('board_topics', kwargs={'pk': self.pk})

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()

    def __str__(self):
        return self.name


class Topic(models.Model):
    """Topic Model"""
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{}_{}'.format(self.pk, self.subject)


class Post(models.Model):
    """Post Model"""
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL)

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)
