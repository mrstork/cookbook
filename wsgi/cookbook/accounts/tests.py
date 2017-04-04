from django.test import Client, TestCase
from django.core import mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


def create_user(email, password):
    user = User.objects.create_user(email, email=email)
    user.set_password(password)
    user.is_active = True
    user.save()
    authenticate(username=email, password=password)


class TestRequestAccount(TestCase):

    def test_request_account(self):
        test_email = 'test@test.com'
        client = Client()
        response = client.post('/accounts/request_account', {'email': test_email})
        self.assertEqual(response.status_code, 200)

        # Registration email sent
        self.assertEqual(len(mail.outbox), 1)

        # User added to the database
        self.assertEqual(User.objects.count(), 1)

        # New user cannot login
        user = User.objects.get(id=1)
        self.assertEqual(user.email, test_email)
        self.assertFalse(user.is_active)

    def tearDown(self):
        mail.outbox = []
        User.objects.all().delete()


# class TestValidateAccount(TestCase):
#
#     def setUp(self):
#         # create two users
#         pass
#
#     def test_incorrect_user(self):
#         pass
#
#     def test_incorrect_key(self):
#         pass
#
#     def test_user_key_mismatch(self):
#         pass
#
#     def test_happy_path(self):
#         pass
#
#     def tearDown(self):
#         mail.outbox = []
#         User.objects.all().delete()
