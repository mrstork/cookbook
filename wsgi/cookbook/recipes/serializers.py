import json
from slugify import slugify
from rest_framework import serializers
from .models import Recipe, RecipeIngredient, RecipeEquipment, RecipeInstruction

class RecipeEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeEquipment
        fields = ('name',)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ('name',)


class RecipeInstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeInstruction
        fields = ('description', 'order',)


class RecipeSerializer(serializers.ModelSerializer):
    equipment = RecipeEquipmentSerializer(read_only=True, many=True)
    ingredients = RecipeIngredientSerializer(read_only=True, many=True)
    instructions = RecipeInstructionSerializer(read_only=True, many=True)
    class Meta:
        model = Recipe
        fields = (
            'title',
            'user',
            'slug',
            'description',
            'serves',
            'time',
            'ingredients',
            'equipment',
            'instructions',
            'draft',
        )

def save_recipe(request, id=None):
    body = request.body.decode('utf-8')
    data = json.loads(body)
    data['user'] = request.user.pk
    if id:
        recipe = Recipe.objects.get(id=id)
        serializer = RecipeSerializer(recipe, data=data)
    else:
        serializer = RecipeSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        # TODO: send error back to user
        print(serializer.errors)
