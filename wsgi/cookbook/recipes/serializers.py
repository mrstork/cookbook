from rest_framework import serializers
from recipes.models import Recipe, RecipeIngredient, RecipeEquipment, RecipeInstruction

class RecipeEquipmentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = RecipeEquipment
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = RecipeIngredient
        fields = '__all__'


class RecipeInstructionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = RecipeInstruction
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    equipment = RecipeEquipmentSerializer(many=True, required=False)
    ingredients = RecipeIngredientSerializer(many=True, required=False)
    instructions = RecipeInstructionSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        exclude = ('slug', 'date_created', )


    def create(self, validated_data):
        equipment_data = validated_data.pop('equipment')
        ingredients_data = validated_data.pop('ingredients')
        instructions_data = validated_data.pop('instructions')

        recipe = Recipe.objects.create(**validated_data)

        for data in equipment_data:
            equipment = RecipeEquipment.objects.create(**data)
            recipe.equipment.add(equipment)

        for data in ingredients_data:
            ingredient = RecipeIngredient.objects.create(**data)
            recipe.ingredients.add(ingredient)

        for data in instructions_data:
            instruction = RecipeInstruction.objects.create(**data)
            recipe.instructions.add(instruction)

        return recipe


    def update(self, instance, validated_data):
        # Equipment - create or update
        if 'equipment' in validated_data:
            equipment_data = validated_data.pop('equipment')

            for data in equipment_data:
                if 'id' in data:
                    equipment = RecipeEquipment(**data)
                    equipment.save()
                else:
                    equipment = RecipeEquipment.objects.create(**data)
                    instance.equipment.add(equipment)


        # Ingredients - create or update
        if 'ingredients' in validated_data:
            ingredients_data = validated_data.pop('ingredients')

            for data in ingredients_data:
                if 'id' in data:
                    ingredient = RecipeIngredient(**data)
                    ingredient.save()
                else:
                    ingredient = RecipeIngredient.objects.create(**data)
                    instance.ingredients.add(ingredient)

        # Instructions - create or update
        if 'instructions' in validated_data:
            instructions_data = validated_data.pop('instructions')

            for data in instructions_data:
                if 'id' in data:
                    instruction = RecipeInstruction(**data)
                    instruction.save()
                else:
                    instruction = RecipeInstruction.objects.create(**data)
                    instance.instructions.add(instruction)

        # Update recipe model
        Recipe.objects.filter(id=instance.id).update(**validated_data)

        # Image field needs explicit save
        if 'image' in validated_data:
            instance.image = validated_data['image']
            instance.save()

        return instance


    def to_representation(self, instance):
        ret = super(RecipeSerializer, self).to_representation(instance)
        ret['username'] = instance.user.username
        return ret
