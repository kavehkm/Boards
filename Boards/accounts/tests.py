# django
from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
# internal
from . import views
from .forms import SignupForm


class SignupTests(TestCase):
    """Signup View Tests"""
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_signup_resolves(self):
        view = resolve('/accounts/signup')
        self.assertEqual(view.func, views.signup)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignupForm)


class SuccessfulSignupTests(TestCase):
    """Successful Signup Tests"""
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'test',
            'email': 'test@gmail.com',
            'password1': 'secretpassword',
            'password2': 'secretpassword'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')

    def test_redirection(self):
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignupTests(TestCase):
    """Invalid Signup Tests"""
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})

    def test_signup_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_done_create_user(self):
        self.assertFalse(User.objects.exists())
