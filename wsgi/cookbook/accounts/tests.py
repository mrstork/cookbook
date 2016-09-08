from django.test import TestCase
from django.core import mail

from django.contrib.auth.models import User
from django.contrib.auth import authenticate


def create_user(email, password):
    user = User.objects.create_user(email, email=email)
    user.set_password(password)
    user.is_active = True
    user.save()
    authenticate(username=email, password=password)

# request account but cannot sign in


class TestAccountRequestEmail(TestCase):

    def setUp(self):
        mail.outbox = []
        pass

    def test_seding_email(self):
        pass

    def tearDown(self):
        mail.outbox = []


class TestAccountRequest(TestCase):

    def setUp(self):
        # create two users
        pass

    def test_incorrect_user(self):
        pass

    def test_incorrect_key(self):
        pass

    def test_user_key_mismatch(self):
        pass

    def test_happy_path(self):
        pass

    def tearDown(self):
        # delete all users
        pass
