from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import Client, TestCase
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

def create_user(email, password):
    user = User.objects.create_user(email, email=email)
    user.set_password(password)
    user.is_active = True
    user.save()
    authenticate(username=email, password=password)

def build_validation_url(user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user),
    return '/accounts/create_account/{}/{}/'.format(uidb64.decode('ascii'), token[0])

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


class TestAccountValidation(TestCase):

    def setUp(self):
        self.client = Client()

        self.user1 = {'username': 'username1', 'email': 'test1@test.com', 'password': 'password'}
        self.user2 = {'username': 'username2', 'email': 'test2@test.com', 'password': 'password'}
        self.user3 = {'username': 'username3', 'email': 'test3@test.com', 'password': 'password'}

        create_user(self.user1['email'], self.user1['password'])
        response = self.client.post('/accounts/request_account', {'email': self.user2['email']})
        response = self.client.post('/accounts/request_account', {'email': self.user3['email']})

        self.user1_object = User.objects.get(email=self.user1['email'])
        self.user2_object = User.objects.get(email=self.user2['email'])
        self.user3_object = User.objects.get(email=self.user3['email'])

    def test_starting_state(self):
        self.user1_object.refresh_from_db()
        self.user2_object.refresh_from_db()
        self.user3_object.refresh_from_db()

        self.assertTrue(self.user1_object.is_active)
        self.assertFalse(self.user2_object.is_active)
        self.assertFalse(self.user3_object.is_active)

    def test_account_revalidation(self):
        url = build_validation_url(self.user1_object)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.test_starting_state()

        response = self.client.post(url, {'username': self.user1['username'], 'password': self.user1['password']})
        self.assertEqual(response.status_code, 200)
        self.test_starting_state()

        # Verify that username was updated in database
        self.assertEqual(self.user1_object.username, self.user1['username'])

    def test_account_validation(self):
        self.test_starting_state()

        url = build_validation_url(self.user2_object)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Verify nothing was changed yet
        self.test_starting_state()

        response = self.client.post(url, {'username': self.user2['username'], 'password': self.user2['password']})
        self.assertEqual(response.status_code, 200)

        # Resync models
        self.user1_object.refresh_from_db()
        self.user2_object.refresh_from_db()
        self.user3_object.refresh_from_db()

        # Assert only 1 user was changed to active
        self.assertTrue(self.user1_object.is_active)
        self.assertTrue(self.user2_object.is_active)
        self.assertFalse(self.user3_object.is_active)

        self.assertEqual(self.user2_object.username, self.user2['username'])

    def tearDown(self):
        mail.outbox = []
        User.objects.all().delete()
