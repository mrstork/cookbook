from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class RequestAccountForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@email.com',
        }))

    def get_or_create_user(self):
        email = self.cleaned_data['email']

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            user = User.objects.create_user(email, email=email)
            user.is_active = False
            user.save()

        return user

    def send_confirmation_email(self, user):
        from_email = 'support@cookbook-stork.rhcloud.com'
        subject = 'Request to join'
        context = {
            'user': user,
            'email': user.email,
            'base_url': settings.BASE_URL,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        }
        body = loader.render_to_string('request_account_email.html', context)
        email_message = EmailMultiAlternatives(subject, body, from_email, [user.email])
        email_message.content_subtype = 'html'
        email_message.send()


class ConfirmAccountForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100,
                                 widget=forms.TextInput(attrs={'required': 'true', 'autofocus': ''}))
    first_name = forms.CharField(label='First Name', max_length=100,
                                 widget=forms.TextInput(attrs={'required': 'true'}))
    last_name = forms.CharField(label='Last Name', max_length=100,
                                widget=forms.TextInput(attrs={'required': 'true'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'required': 'true'}))

    def confirm_account(self, user):
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.set_password(self.cleaned_data['password'])
        user.is_active = True
        user.save()
        return authenticate(username=user.username, password=self.cleaned_data['password'])
