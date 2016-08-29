from django.shortcuts import render
from django.http import HttpResponse
from .serializers import add_recipe
from .models import Recipe


def list_view(request):
    context = {
        'recipes': Recipe.objects.all()
    }
    return render(request, 'list-recipes.html', context)


def add_view(request):
    context = {}
    if request.method == 'POST':
        add_recipe(request)
        return HttpResponse('Recipe Added')
    return render(request, 'edit-recipe.html', context)


def edit_view(request):
    context = {}
    return render(request, 'edit-recipe.html', context)


def detail_view(request):
    context = {}
    return render(request, 'view-recipe.html', context)
