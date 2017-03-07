import json
from slugify import slugify
from .models import Recipe, RecipeIngredient, RecipeEquipment, RecipeInstruction

def add_recipe(request):
    body = request.body.decode('utf-8')
    data = json.loads(body)
    recipe = Recipe.objects.create(
        user=request.user,
        title=data['title'],
        # TODO: replace slugify with your own slugify function
        slug=slugify(data['title']),
        description=data['description'],
        serves=data['serves'],
        time=data['time'],
    )

    recipe.save()

    for ingredient in data['ingredients']:
        if 'name' in ingredient:
            print(ingredient)
            recipe.ingredients.create(
                name=ingredient['name'],
            )

    for equipment in data['equipment']:
        if 'name' in equipment:
            print(equipment)
            recipe.equipment.create(
                name=equipment['name'],
            )

    for instruction in data['instructions']:
        if 'description' in instruction:
            print(instruction)
            recipe.instructions.create(
                description=instruction['description'],
                order=instruction['order'],
            )

    recipe.save()
