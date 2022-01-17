# django
from django.urls import path
from django.contrib.auth import views as auth_views
# internal
from . import views


urlpatterns = [
    path('signup', views.signup, name='signup'),
]
