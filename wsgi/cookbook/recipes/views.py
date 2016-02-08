from django.shortcuts import render


def list_view(request):
    context = {}
    return render(request, 'list-recipes.html', context)


def add_view(request):
    context = {}
    return render(request, 'edit-recipe.html', context)


def edit_view(request):
    context = {}
    return render(request, 'edit-recipe.html', context)


def detail_view(request):
    context = {}
    return render(request, 'view-recipe.html', context)
