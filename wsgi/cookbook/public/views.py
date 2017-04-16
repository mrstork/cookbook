from django.shortcuts import render
from accounts.forms import RequestAccountForm


def index(request):
    return render(request, 'index.html')
