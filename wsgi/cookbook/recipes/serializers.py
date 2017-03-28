from rest_framework import serializers
from recipes.models import Recipe, RecipeIngredient, RecipeEquipment, RecipeInstruction

class RecipeEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeEquipment
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = '__all__'


class RecipeInstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeInstruction
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    equipment = RecipeEquipmentSerializer(read_only=True, many=True)
    ingredients = RecipeIngredientSerializer(read_only=True, many=True)
    instructions = RecipeInstructionSerializer(read_only=True, many=True)

    class Meta:
        model = Recipe
        exclude = ('slug', 'date_created', )


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

    def to_representation(self, instance):
        ret = super(RecipeSerializer, self).to_representation(instance)
        ret['username'] = instance.user.username
        return ret
