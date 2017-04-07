from rest_framework import serializers
from recipes.models import Recipe, RecipeIngredient, RecipeEquipment, RecipeInstruction
from recipes.fields import PNGField

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
    image = serializers.ImageField(required=False, _DjangoImageField=PNGField)
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
        # TODO: handle efiiciency of deleting then creating
        # Equipment - create, update, or delete
        if 'equipment' in validated_data:
            equipment_data = validated_data.pop('equipment')

            # Delete
            ids = [item['id'] for item in equipment_data if 'id' in item]
            instance.equipment.exclude(id__in=ids).delete()

            for data in equipment_data:
                # Update
                if 'id' in data:
                    equipment = RecipeEquipment(**data)
                    equipment.save()
                # Create
                else:
                    equipment = RecipeEquipment.objects.create(**data)
                    instance.equipment.add(equipment)


        # Ingredients - create, update, or delete
        if 'ingredients' in validated_data:
            ingredients_data = validated_data.pop('ingredients')

            # Delete
            ids = [item['id'] for item in ingredients_data if 'id' in item]
            instance.ingredients.exclude(id__in=ids).delete()

            for data in ingredients_data:
                # Update
                if 'id' in data:
                    ingredient = RecipeIngredient(**data)
                    ingredient.save()
                # Create
                else:
                    ingredient = RecipeIngredient.objects.create(**data)
                    instance.ingredients.add(ingredient)

        # Instructions - create, update, or delete
        if 'instructions' in validated_data:
            instructions_data = validated_data.pop('instructions')

            # Delete
            ids = [item['id'] for item in instructions_data if 'id' in item]
            instance.instructions.exclude(id__in=ids).delete()

            for data in instructions_data:
                # Update
                if 'id' in data:
                    instruction = RecipeInstruction(**data)
                    instruction.save()
                # Create
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

    def validate_image(self, value):
        print(value)
        return value

    def to_representation(self, instance):
        ret = super(RecipeSerializer, self).to_representation(instance)
        ret['username'] = instance.user.username
        return ret
