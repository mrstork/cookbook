import json
from .models import Recipe


def add_recipe(request):
    body = request.body.decode('utf-8')
    data = json.loads(body)
    # {'equipment': [{'placeholder': 'Wok'}, {'placeholder': 'Broom'}, {'placeholder': 'Magnifying Glass'}], 'title': 'asfasfasf', 'instructions': [{'placeholder': 'Step 1'}, {'placeholder': 'Step 2'}, {'placeholder': 'Step 3'}], 'ingredients': [{'name_placeholder': 'Gummy Worms', 'quantity_placeholder': 18, 'measurement_placeholder': 'oz.'}, {'name_placeholder': 'Socks', 'quantity_placeholder': 3, 'measurement_placeholder': 'pairs'}, {'name_placeholder': 'Smelly Cheese', 'quantity_placeholder': 15, 'measurement_placeholder': 'block'}]}
    Recipe.objects.create(
        user=request.user,
        title=data['title'],
        description=data['description'],
    )
