# from slugify import slugify
from rest_framework import serializers
from recipes.models import Recipe, RecipeIngredient, RecipeEquipment, RecipeInstruction

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
    id = serializers.IntegerField(read_only=True)
    equipment = RecipeEquipmentSerializer(read_only=True, many=True)
    ingredients = RecipeIngredientSerializer(read_only=True, many=True)
    instructions = RecipeInstructionSerializer(read_only=True, many=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
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

    def create(self, validated_data):
        # equipment = RecipeEquipment.objects.create(**validated_data)
        # ingredients = RecipeIngredient.objects.create(**validated_data)
        # instructions = RecipeInstruction.objects.create(**validated_data)
        return Recipe.objects.create(
            **validated_data,
            # equipment=equipment,
            # ingredients=ingredients,
            # instructions=instructions,
        )
