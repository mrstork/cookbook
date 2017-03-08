from django.shortcuts import render
from accounts.forms import RequestAccountForm


def index(request):
    context = {
        'request_account_form': RequestAccountForm()
    }
    return render(request, 'index.html', context, content_type="text/html")
