from django.db import models
from django.conf import settings


class RecipeIngredient(models.Model):
    name = models.CharField(max_length=500)


class RecipeEquipment(models.Model):
    name = models.CharField(max_length=500)


class RecipeInstruction(models.Model):
    description = models.CharField(max_length=500)
    order = models.IntegerField()


class Recipe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    # TODO: Shrink max lengths once there are a few recipes in the database as examples
    title = models.CharField(max_length=1000, null=True, blank=True)
    slug = models.CharField(max_length=1000, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    serves = models.CharField(max_length=100, null=True, blank=True)
    time = models.FloatField(max_length=100, null=True, blank=True)
    ingredients = models.ForeignKey(RecipeIngredient, null=True, blank=True)
    equipment = models.ForeignKey(RecipeEquipment, null=True, blank=True)
    instructions = models.ForeignKey(RecipeInstruction, null=True, blank=True)
