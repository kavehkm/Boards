# django
from django.urls import path
# internal
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('boards/<int:pk>', views.board_topics, name='board_topics')
]
