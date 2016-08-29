from django.shortcuts import render, redirect
from accounts.forms import RequestAccountForm


def index(request):
    if request.user.is_authenticated():
        return redirect('list_recipes')

    context = {
        'request_account_form': RequestAccountForm()
    }
    return render(request, 'index.html', context, content_type="text/html")
