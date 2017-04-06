from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UsernameField, AuthenticationForm as DjangoAuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from premailer import transform

class RequestAccountForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True})
    )

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
        from_email = settings.DEFAULT_FROM_EMAIL
        subject = 'Ryōrisho - Registration confirmation'
        context = {
            'user': user,
            'email': user.email,
            'base_url': settings.BASE_URL,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        }
        body = loader.render_to_string('request_account_email.html', context)
        email_message = EmailMultiAlternatives(subject, transform(body), from_email, [user.email])
        email_message.content_subtype = 'html'
        email_message.send()


class ConfirmAccountForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'true', 'autofocus': ''})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'true'})
    )

    def confirm_account(self, user):
        # TODO: username cannot contain symbols
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user.username = username
        user.set_password(password)
        user.is_active = True
        user.save()
        return authenticate(username=user.username, password=password)


class AuthenticationForm(DjangoAuthenticationForm):
    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True})
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            if '@' in username:
                user = User.objects.filter(email=username).first()
            else:
                user = User.objects.filter(username=username).first()

            if user is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.user_cache = authenticate(self.request, username=user.username, password=password)
                if self.user_cache is None:
                    raise forms.ValidationError(
                        self.error_messages['invalid_login'],
                        code='invalid_login',
                        params={'username': self.username_field.verbose_name},
                    )
                else:
                    self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
