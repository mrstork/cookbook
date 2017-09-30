from .forms import RequestAccountForm, ConfirmAccountForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import login
from django.shortcuts import render, redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.http import require_POST
from accounts.forms import RequestAccountForm, AuthenticationForm


def register(request):
    context = {
        'form': RequestAccountForm()
    }

    if request.method == 'POST':
        return request_account(request)

    return render(request, 'register.html', context)


def authentication(request):
    if request.user.is_authenticated():
        return redirect('recipe-list', user=request.user)

    response = login(request,
                     authentication_form=AuthenticationForm,
                     template_name='login.html')
    return response


@require_POST
def request_account(request):
    form = RequestAccountForm(request.POST)

    if form.is_valid():
        user = form.get_or_create_user()

        if not user.is_active:
            form.send_confirmation_email(user)

    return render(request, 'thank-you.html')


def confirm_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        return render(request, 'invalid-token.html', status=403)

    form = ConfirmAccountForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.confirm_account(user)
        if user is not None:
            login(request, user)
            return render(request, 'welcome.html')

    context = {
        'uidb64': uidb64,
        'token': token,
        'email': user.email,
        'form': form,
    }

    return render(request, 'confirm-account.html', context)


# TODO: edit profile view: change password, email, username, ...


@login_required
@require_POST
def delete_account(request, password):
    user = request.user
    logout(request)
    user.delete()
    return render(request, 'goodbye.html')


def logout_view(request):
    logout(request)
    return render(request, 'logout.html')
