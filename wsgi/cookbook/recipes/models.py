from django.db import models
from django.conf import settings

class RecipeIngredient(models.Model):
    name = models.CharField(max_length=500)


class RecipeEquipment(models.Model):
    name = models.CharField(max_length=500)


class RecipeInstruction(models.Model):
    description = models.CharField(max_length=500)
    order = models.IntegerField()

    # class Meta:
    #     ordering = ('order', )


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
    time = models.CharField(max_length=100, null=True, blank=True)
    ingredients = models.ManyToManyField(RecipeIngredient)
    equipment = models.ManyToManyField(RecipeEquipment)
    instructions = models.ManyToManyField(RecipeInstruction)

    def __str__(self):
        return self.slug

    # class Meta:
    #     unique_together = ('user', 'slug')
