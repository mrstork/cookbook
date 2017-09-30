from accounts.tests import create_user
from django.contrib.auth.models import User
from django.test import TestCase
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from recipes.views import new_recipe

class TestNewRecipe(TestCase):
    def setUp(self):
        create_user('email@email.com', 'password')

    def test_new_recipe(self):
        new_recipe(1)
        self.assertEqual(Recipe.objects.count(), 1)

    def tearDown(self):
        Recipe.objects.all().delete()
        User.objects.all().delete()


class TestModelDeleteCascade(TestCase):
    def setUp(self):
        create_user('email@email.com', 'password')
        new_recipe(1)

    def test_delete_user_cascade(self):
        User.objects.all().delete()
        self.assertEqual(Recipe.objects.count(), 0)


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
        }
        serializer = RecipeSerializer(data=recipe_json)
        serializer.is_valid()
        serializer.save()

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

    def test_fail_add(self):
        recipe_json = {}
        serializer = RecipeSerializer(data=recipe_json)
        serializer.is_valid()
        # user is a required field so adding should fail
        self.assertNotEqual(len(serializer.errors), 0)

    def test_edit(self):
        new_recipe(1)
        recipe = Recipe.objects.get(id=1)
        serializer = RecipeSerializer(recipe)

        test_title = 'Something else'
        serializer = RecipeSerializer(recipe, data={
            'title': test_title,
            'user': 1,
        })
        self.assertTrue(serializer.is_valid())
        serializer.save()

        # resync with db and check that values made it into the database
        recipe.refresh_from_db()
        self.assertEqual(test_title, recipe.title)

    def tearDown(self):
        User.objects.all().delete()
