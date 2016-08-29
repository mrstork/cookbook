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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    serves = models.CharField(max_length=100, null=True, blank=True)
    time = models.FloatField(null=True, blank=True)
    ingredients = models.ForeignKey(RecipeIngredient, null=True, blank=True)
    equipment = models.ManyToManyField(Equipment, blank=True)
    instructions = models.ForeignKey(Instruction, null=True, blank=True)
