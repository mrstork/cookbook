from django.db import models
from django.conf import settings


class Ingredient(models.Model):
    name = models.CharField(max_length=100)


class Equipment(models.Model):
    name = models.CharField(max_length=100)


class Measurement(models.Model):
    name = models.CharField(max_length=100)


class RecipeIngredient(models.Model):
    quantity = models.FloatField()
    measurement = models.ForeignKey(Measurement)
    ingredient = models.ForeignKey(Ingredient)


class Instruction(models.Model):
    description = models.CharField(max_length=300)
    order = models.IntegerField()


class Recipe(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    serves = models.CharField(max_length=100)
    time = models.FloatField()
    ingredients = models.ForeignKey(RecipeIngredient)
    equipment = models.ManyToManyField(Equipment)
    instructions = models.ForeignKey(Instruction)
