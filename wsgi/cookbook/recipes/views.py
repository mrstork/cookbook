from .models import Recipe
from .serializers import add_recipe
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render


@login_required
def list_view(request):
    context = {
        'recipes': Recipe.objects.all()
    }
    return render(request, 'list-recipes.html', context)


@login_required
def add_view(request):
    context = {}
    if request.method == 'POST':
        add_recipe(request)
        return HttpResponse('Recipe Added')
    return render(request, 'edit-recipe.html', context)


@login_required
def edit_view(request):
    context = {}
    return render(request, 'edit-recipe.html', context)


# @login_required
# def detail_view(request):
#     context = {}
#     return render(request, 'view-recipe.html', context)

@login_required
def detail_view(request, slug):
    recipe = Recipe.objects.all()[0]
    print(recipe)
    print(recipe.title)
    context = {
        'recipe': recipe
    }
    return render(request, 'view-recipe.html', context)
