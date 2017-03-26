from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from rest_framework.parsers import MultiPartParser
from rest_framework.renderers import JSONRenderer

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
    try:
        recipe = Recipe.objects.get(id=id)
    except Recipe.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = RecipeSerializer(recipe)
        context = {
            'recipe': JSONRenderer().render(serializer.data)
        }
        return render(request, 'edit-recipe.html', context)

    elif request.method == 'POST':
    #     data = MultiPartParser().parse(request)
        return HttpResponse(status=500)
        # serializer = RecipeSerializer(recipe, data=data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return JsonResponse(serializer.data)

    # body = request.body.decode('utf-8')
    # data = json.loads(body)
    # data['user'] = request.user.pk
    # print(data)
    # if id:
    #     recipe = Recipe.objects.get(id=id)
    #     serializer = RecipeSerializer(recipe, data=data)
    # else:
    #     serializer = RecipeSerializer(data=data)
    # if serializer.is_valid():
    #     serializer.save()
    # else:
    #     # TODO: send error back to user
    #     print(serializer.errors)


def detail_view(request, user, id):
    recipe = Recipe.objects.get(id=id)
    # TODO: default to something if the recipe is not found
    context = {
        'recipe': recipe
    }
    return render(request, 'view-recipe.html', context)
