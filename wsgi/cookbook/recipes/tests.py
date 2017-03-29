from django.test import TestCase
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from accounts.tests import create_user

class TestRecipeSerializers(TestCase):
    def setUp(self):
        create_user('email@email.com', 'password')

    def test_add(self):
        recipe_json = {
            'title': 'Test Recipe',
            'user': 1,
            'description': 'description',
            'serves': 'Serves 5',
            'time': '30 min',
            'equipment': [
                { 'name': '...' },
            ],
            'ingredients': [
                { 'name': '...' },
            ],
            'instructions': [
                { 'description': '...' },
            ],
        };
        serializer = RecipeSerializer(data=recipe_json);
        serializer.is_valid();
        serializer.save();

        # check if in database
        self.assertEqual(Recipe.objects.count(), 1)

        # check that values match
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe_json['title'], recipe.title)
        self.assertEqual(recipe_json['description'], recipe.description)
        self.assertEqual(recipe_json['serves'], recipe.serves)
        self.assertEqual(recipe_json['time'], recipe.time)

        # check that nested values match
        self.assertEqual(recipe.equipment.count(), 1)
        self.assertEqual(recipe_json['equipment'][0]['name'], recipe.equipment.all()[0].name)

        self.assertEqual(recipe.ingredients.count(), 1)
        self.assertEqual(recipe_json['ingredients'][0]['name'], recipe.ingredients.all()[0].name)

        self.assertEqual(recipe.instructions.count(), 1)
        self.assertEqual(recipe_json['instructions'][0]['description'], recipe.instructions.all()[0].description)
