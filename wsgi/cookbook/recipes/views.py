from .models import Recipe
from .serializers import save_recipe
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

def base_view(request):
    # TODO: make a complete list or a trending list
    return redirect('list-recipes', request.user)


def list_view(request, user):
    context = {
        'recipes': Recipe.objects.filter(user__username=user)
    }
    return render(request, 'list-recipes.html', context)


@login_required
def add_view(request):
    # TODO: merge this with edit view
    context = {}
    if request.method == 'POST':
        save_recipe(request)
        return HttpResponse('Recipe created.')
    return render(request, 'edit-recipe.html', context)


@login_required
def edit_view(request, user, id):
    recipe = Recipe.objects.get(id=id)
    # TODO: default to something if the recipe is not found
    # get object or 404
    context = {
        'recipe': recipe
    }
    if request.method == 'POST':
        save_recipe(request, id)
        return HttpResponse('Recipe saved.')
    return render(request, 'edit-recipe.html', context)


def detail_view(request, user, id):
    recipe = Recipe.objects.get(id=id)
    # TODO: default to something if the recipe is not found
    context = {
        'recipe': recipe
    }
    return render(request, 'view-recipe.html', context)
