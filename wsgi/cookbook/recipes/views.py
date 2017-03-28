from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

def base_view(request):
    # TODO: make a complete list or a trending list
    return redirect('recipe-list', request.user)


@login_required
def add_view(request):
    serializer = RecipeSerializer(data={
        'title': 'New Recipe',
        'user': request.user.pk,
        'description': 'Write a description for your brilliant new recipe that will make your mouth water',
        'serves': 'Serves 5',
        'time': '30 - 40 min',
        # TODO: Add nested data back in. For some reason serializer isn't picking up the data
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
    return redirect('recipe-detail', request.user, recipe.id)


class RecipeList(APIView):
    def get(self, request, user, format=None):
        recipes = Recipe.objects.all()
        # recipes = Recipe.objects.filter(user=user)
        serializer = RecipeSerializer(recipes, many=True)
        context = {
            'recipes': serializer.data
        }
        return render(request, 'list-recipes.html', context)


class RecipeDetail(APIView):
    parser_classes = (MultiPartParser, FormParser,)

    def get_object(self, pk):
        try:
            return Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            raise Http404

    def get(self, request, user, pk, format=None):
        recipe = self.get_object(pk)

        if request.user == recipe.user:
            serializer = RecipeSerializer(recipe)
            context = {
                'recipe': JSONRenderer().render(serializer.data)
            }
            return render(request, 'edit-recipe.html', context)

        return render(request, 'view-recipe.html', { 'recipe': recipe })

    def post(self, request, user, pk, format=None):
        recipe = self.get_object(pk)
        serializer = RecipeSerializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user, pk, format=None):
        recipe = self.get_object(pk)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
