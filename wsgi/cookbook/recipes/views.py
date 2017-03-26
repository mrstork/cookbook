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
    serializer = RecipeSerializer(data={
        'title': 'New Recipe',
        'user': request.user.pk,
        'description': 'Write a description for your brilliant new recipe that will make your mouth water',
        'serves': 'Serves 5',
        'time': '30 - 40 min',
        # 'equipment': [
        #   { 'name': 'Rolling pin' },
        #   { 'name': 'Cake tin' },
        # ],
        # 'ingredients': [
        #   { 'name': '3 cups of flour' },
        #   { 'name': '1 stick of butter' },
        # ],
        # 'instructions': [
        #   { 'description': 'This is what you do first...', 'order': 0 },
        # ],
    });
    serializer.is_valid();
    recipe = serializer.save();
    return redirect('edit-recipe', request.user, recipe.id)


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
    try:
        recipe = Recipe.objects.get(id=id)
    except Recipe.DoesNotExist:
        return HttpResponse(status=404)

    context = {
        'recipe': recipe
    }
    return render(request, 'view-recipe.html', context)
