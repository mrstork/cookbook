from django.db import models
from django.conf import settings

class RecipeIngredient(models.Model):
    name = models.CharField(max_length=500)


class RecipeEquipment(models.Model):
    name = models.CharField(max_length=500)


class RecipeInstruction(models.Model):
    description = models.CharField(max_length=500)
    # TODO: see if ordering necessary
    order = models.IntegerField()

    # class Meta:
    #     ordering = ('order', )


class Recipe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to='recipe-images/', blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    slug = models.CharField(max_length=1000, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    serves = models.CharField(max_length=100, blank=True, null=True)
    time = models.CharField(max_length=100, blank=True, null=True)
    ingredients = models.ManyToManyField(RecipeIngredient)
    equipment = models.ManyToManyField(RecipeEquipment)
    instructions = models.ManyToManyField(RecipeInstruction)
    draft = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    # TODO: Shrink max lengths of fields once there are a few recipes in the database as examples

    def __str__(self):
        return self.title + ' - ' + self.description
